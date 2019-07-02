
# encoding: utf-8
import logging
from utils.logger import MyLogger
from utils import common
from utils import adbShell
import os
import unittest
import time

PATH = os.path.dirname(os.path.abspath(__file__))
GTPath = "/sdcard/GT/GW/com.imo.android.imoimalpha/unknow/"
GT_Log_Path = PATH+'\\'+'GT\\'
#GT_Log_Path = PATH+'/'+'GT/'
log = MyLogger(logging.DEBUG, logging.DEBUG)
IsUseTwoPhone = False
class AndroidTest(unittest.TestCase):
    caseName = ''

    def setUp(self):
        self.driverId = 'a22ec83d'
        self.desired_caps = common.read_cofig('driver', self.driverId)
        self.driver = common.getDriver(self.desired_caps)
        #adbShell.open_gt(self.desired_caps['appPackage'], self.driverId)

        # if IsUseTwoPhone:
        #     self.driverId2 = 'a22ec83d'
        #     self.desired_caps2 = common.read_cofig('driver', self.driverId2)
        #     adbShell.open_gt(self.desired_caps2['appPackage'],  self.driverId2)
        #     self.driver2 = common.getDriver(self.desired_caps2)

    def tearDown(self):
        self.driver.quit()
        filename = self.caseName + self.desired_caps['deviceName']+common.get_data()
        # adbShell.exit_gt(self.desired_caps['appPackage'], self.desired_caps['deviceName'], filename)
        # adbShell.copyfile(GTPath + filename, GT_Log_Path, self.driverId)
        # if IsUseTwoPhone:
        #     self.driver2.quit()
        #     filename2 = self.caseName + self.desired_caps2['deviceName'] + common.get_data()
        #     adbShell.exit_gt(self.desired_caps2['appPackage'], self.desired_caps['deviceName'], filename2)
        #     adbShell.copyfile(GTPath + filename2, GT_Log_Path, self.driverId2)

    def testIntoFeed(self):
        for i in range(200):
            adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/btn_negative', '取消弹窗', True)
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/tv_wording', '进入信息流'))
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/close_button', '返回首页'))
            log.info("testIntoFeed"+str(i))



if __name__ == "__main__":

    #构造测试集
    suite = unittest.TestSuite()
    suite.addTest(AndroidTest("testIntoFeed"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # log.info("拷贝数nnnnn据成功！")

