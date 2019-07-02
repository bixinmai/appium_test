#!/usr/bin/env python

# encoding: utf-8

'''

@author: xiaoxiaohua

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: xiaoxiaohua1008@gmail.com

@software: garner

@file: androidTestCase.py

@time: 2018/8/21 14:56

@desc:

'''
import logging
import multiprocessing
import unittest
import sys
import os
from time import sleep
from conmon import Adb, FileRead
from conmon.Adb import LaunchAPP
from conmon.Logger import MyLogger
from module.FriendModel import EnterRoomByProfile
from module.Login import login
from module.RoomModel import EnterAndOutRoom, GetMicrophone, ChangeRoom, ChangeNewTab, OpenTurntable, EnterMyRoom, \
    FlushLightning, HighGiftEffect, OutOfOtherRoom, Deco, GetLuckyBox

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
GTPath = "/sdcard/GT/GW/sg.bigo.hellotalk/unknow/"
Path_T = "F:\workspace\python\helloyo_GT\GT"
log = MyLogger('F:\\workspace\\python\\helloyo_GT\\log', logging.DEBUG, logging.DEBUG)

numtime = 250

class AndroidTest(unittest.TestCase):
    def setUp(self):
        self.driver = ""
        self.deviceID = ""
        self.driver2 = ""
        self.deviceID2 = ""

        # 如果需要连接两台设备，则IsUseTwoPhone=True，且把对应的设备ID1、ID2的设备号填写；
        # 如果仅连接一台设备，则直接IsUseTwoPhone=False。
        IsUseTwoPhone = False
        if IsUseTwoPhone:
            self.deviceID = "52e1ce04"
            self.deviceID2 = "de02c84e"
        else:
            self.deviceID = Adb.getDeviceID()

        self.driver = FileRead.getDriver(self.deviceID)

        # 打开GT
        # Adb.OpenGT(deviceID=self.deviceID)
        if self.deviceID2:
            # port填写为设备2连接的appnium的端口号
            self.driver2 = FileRead.getDriver(deviceID=self.deviceID2, port="4725")
            # 打开GT
            Adb.OpenGT(deviceID=self.deviceID2)
        self.CaseName = ""

    def tearDown(self):

        self.driver.quit()
        # 退出GT，保存GT数据
        # Adb.ExitGT(fileName=self.CaseName+self.deviceID,deviceID=self.deviceID)
        # Adb.CopyFile(GTPath,Path_T,deviceID=self.deviceID)
        # 清空APP数据
        # Adb.clearApp(deviceID=self.deviceID)
        if self.driver2 :
            self.driver2.quit()
            # 退出GT，保存GT数据
            Adb.ExitGT(fileName=self.CaseName + self.deviceID2,deviceID=self.deviceID2)
            Adb.CopyFile(GTPath, Path_T, deviceID = self.deviceID2)
        #     # 清空APP数据
        #     Adb.clearApp(deviceID=self.deviceID2)


if __name__ == "__main__":
    # suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTest)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(AndroidTest("testLogin"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
