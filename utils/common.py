#!/usr/bin/env python
# from appium import webdriver
from utils.myconf import myconf
import os,time
from appium import webdriver

PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def read_cofig(file, config):
    fileName = PATH+'\\config\\'+file+'.ini'
    #fileName = PATH+'/config/'+file+'.ini'
    if not os.path.exists(fileName):
        print("当前没有该文件")
        return
    cf = myconf()
    cf.read(fileName)
    item = cf.items(config)
    kvs = dict(item)
    return kvs

def getDriver(desired_caps):
    driver = webdriver.Remote('http://127.0.0.1:'+desired_caps['port']+'/wd/hub', desired_caps)
    return driver

def get_data():
    now = time.localtime(time.time())
    return time.strftime('%Y%m%d%H%M%S', now)


if __name__ == "__main__":
    getDriver('88LX01KWG')
    #read_cofig('driver', 'a22ec83d')