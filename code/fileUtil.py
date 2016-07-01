#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
from datetime import datetime
import urllib.request
import logging
import traceback
#本地验证码临时存放目录
imgPath='E:/private/image/'
#根据路径下载验证码图片并返回本地的保存路径
def downCode(verifyCodeUrl):
    #下载验证码图片
#     print('开始获取验证码：%s' % verifyCodeUrl)
    try:
        f = urllib.request.urlopen(verifyCodeUrl)
        data = f.read()
        tempFileName = datetime.now().strftime('%Y%m%d%H%M%S%f')+'.jpg'
        with open(imgPath+tempFileName, "wb") as code:
            code.write(data)
        print('下载验证码图片成功,保存路径：%s' % imgPath+tempFileName)
        return imgPath+tempFileName
    except Exception as e:
        print('Error:',e)
        traceback.print_exc()
        logging.exception(e)
def appendTextFile(filePath,data):
    file_object = open(filePath, 'a')
    file_object.write(data)
    file_object.close()
if __name__=='__main__':
    for i in range(1000):
        codeLocalPath = downCode('http://mygiftcard.jd.com/giftcard/JDVerification.aspx?uid=7f30cdf4-3f2f-4471-8c14-5a94533955d2&t=0.3688577947670343')
        print('下载路径为：%s' % codeLocalPath)
