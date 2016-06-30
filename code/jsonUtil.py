#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
import json
import urllib.request

#获取json串的多级属性
def getAttr(jsonBytes,*attrNames):
    #内部函数
    def getJsonObj(jsonBytes):
        jsonObj = json.loads(jsonBytes.decode('utf-8'))
        return jsonObj
    #初始化res为对象
    res = getJsonObj(jsonBytes);
    for attrName in attrNames:
        res = res[attrName]
    return res
if __name__=='__main__':
    htmlSource = urllib.request.urlopen(r'http://api.douban.com/v2/book/isbn/9787218087351').read()
    print(getAttr(htmlSource,'rating'))
    print(type(getAttr(htmlSource,'rating')))
    print(getAttr(htmlSource,'images','large'))
    print(type(getAttr(htmlSource,'images','large')))

    
    
