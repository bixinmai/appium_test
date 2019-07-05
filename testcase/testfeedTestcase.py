
# encoding: utf-8
import logging
from utils.logger import MyLogger
from utils import common
from utils import adbShell
import os
import unittest
from utils.jarfile import Jar
import time



class AndroidTest(unittest.TestCase):
    caseName = ''

    def setUp(self):
        self.driverId = 'a22ec83d'
        self.desired_caps = common.read_cofig('driver', self.driverId)
        self.driver = common.getDriver(self.desired_caps)


    def tearDown(self):
        self.driver.quit()

    def testIntoFeed(self):
        for i in range(2):
            adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/btn_negative', '取消弹窗', True)
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/tv_wording', '进入信息流'))
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/close_button', '返回首页'))


if __name__ == "__main__":

    #构造测试集
    suite = unittest.TestSuite()
    suite.addTest(AndroidTest("testIntoFeed"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)



