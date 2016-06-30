import urllib
import http.cookiejar
import socket
from bs4 import BeautifulSoup
import traceback
# from datetime import datetime
from PIL import Image
import fileUtil
import windowsUtil

RETRY_COUNT=5
loginPageUrl = "https://passport.jd.com/new/login.aspx"
loginPostUrl = "http://passport.jd.com/uc/loginService"
pwdFilePath = "E:/private/pwd.txt"
UUID=''
userName='13426314653'
password=''
imgPath='E:/private/image/'
#定义连接函数，有超时重连功能
def init():
    global password
    file_object = open(pwdFilePath)
    try:
        all_the_text = file_object.read()
        password =  all_the_text
        print('got passwd:%s' % password)
    except Exception as e:
        print("Error:",e)
        traceback.print_exc()
    finally:
        file_object.close( )
def Navigate(url,data={}):           
    tryTimes = 0
    while True:
        if (tryTimes > RETRY_COUNT):
            print("尝试%s次之后仍无法链接网络，程序终止" % RETRY_COUNT)
            break
        try:
            if (data=={}):
                req = urllib.request.Request(url)
            else:
                req = urllib.request.Request(url,urllib.parse.urlencode(data).encode('utf-8'))
            req = urllib.request.urlopen(req).read()
            tryTimes = tryTimes +1
        except socket.error:
            print("连接失败，尝试重新连接")
            traceback.print_exc()
        else:
            break
    return req   
#处理cookie
def processCookie():
    try:
        cookie = http.cookiejar.CookieJar()
        cookieProc = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(cookieProc)
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        urllib.request.install_opener(opener)
    except Exception as e:
        print("Error",e)
        traceback.print_exc()
#获取和组装post请求数据
def packagePostData():
    login = Navigate(loginPageUrl)
    print('获取到登录页的内容：')
    print(login)
    loginSoup = BeautifulSoup(login,'html.parser')
    #查找登陆参数中的uuid
    uuid = loginSoup.find_all("form")[0].find_all("input")[0]['value']
    print('uuid: %s' % uuid)
    global UUID
    UUID=uuid
    #获取form表单里的隐藏域信息
    name4 = loginSoup.find_all("form")[0].find_all("input")[4]['name']  
    value4 = loginSoup.find_all("form")[0].find_all("input")[4]['value']
    print(name4,value4)
    name5 = loginSoup.find_all("form")[0].find_all("input")[5]['name']  
    value5 = loginSoup.find_all("form")[0].find_all("input")[5]['value']
    print(name5,value5)
    name6 = loginSoup.find_all("form")[0].find_all("input")[6]['name']  
    value6 = loginSoup.find_all("form")[0].find_all("input")[6]['value']
    print(name6,value6) 
    name7 = loginSoup.find_all("form")[0].find_all("input")[7]['name']  
    value7 = loginSoup.find_all("form")[0].find_all("input")[7]['value']
    print(name7,value7) 
    #print url
    postData = {
      'loginname':userName,
      'nloginpwd':password,
      'loginpwd':password,
      'machineNet':'',
      'machineCpu':'',
      'machineDisk':'', 
       str(name4):str(value4),
       str(name5):str(value5),
       str(name6):str(value6),
       str(name7):str(value7),
      'uuid':uuid,
      'authcode':''
    }
    #下载验证码
    checkPicUrl = 'http:'+loginSoup.find_all("img","verify-code")[0]['src2']
    codeLocalPath = fileUtil.downCode(checkPicUrl)
    image=Image.open(codeLocalPath)
    #打开图片
    image.show()
    checkCode = input("请输入弹出图片中的验证码：") 
    #关闭图片查看器
    windowsUtil.closeWin()
    postData['authcode'] = str(checkCode)
    print('login postData:')
    print(postData)
    return postData
if __name__=='__main__':
    processCookie()
    passportRes = Navigate(loginPostUrl,packagePostData())
    print('login response: %s' % passportRes)
     
      
    