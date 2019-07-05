
# encoding: utf-8
import logging
from utils.logger import MyLogger
from utils import common
from utils import adbShell
import os
import unittest
from utils.jarfile import Jar
import time

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GTPath = "/sdcard/GT/GW/com.imo.android.imoimalpha/unknow/"
GT_Log_Path = PATH+'\\'+'GT\\'
#GT_Log_Path = PATH+'/'+'GT/'
IsUseTwoPhone = True
jar_path = 'F:\\test-gt\\jar\\Monitor.jar'
monitor_package_name = 'sg.bigo.dump.RunMonitor'
packName = "com.imo.android.imoimalpha"
log = MyLogger(logging.DEBUG, logging.DEBUG)


class FeedTest(unittest.TestCase):
    caseName = ''

    def setUp(self):
        self.driverId = 'P7C0218309010307'
        self.desired_caps = common.read_cofig('driver', self.driverId)
        self.driver = common.getDriver(self.desired_caps)

        #用Monitor检测性能
        self.monitorJar = Jar()
        self.monitor = self.monitorJar.StartMonitor(monitor_package_name, jar_path, self.driverId, packName)

        if IsUseTwoPhone:
            self.driverId2 = 'a22ec83d'
            self.desired_caps2 = common.read_cofig('driver', self.driverId2)
            self.driver2 = common.getDriver(self.desired_caps2)

        #用GT检测性能
        #adbShell.open_gt(self.desired_caps['appPackage'], self.driverId)

        # if IsUseTwoPhone:
        #     self.driverId2 = 'a22ec83d'
        #     self.desired_caps2 = common.read_cofig('driver', self.driverId2)
        #     self.driver2 = common.getDriver(self.desired_caps2)
        #     adbShell.open_gt(self.desired_caps2['appPackage'],  self.driverId2)


    def tearDown(self):
        self.driver.quit()
        self.monitorJar.stopMonitor(self.monitor, self.driverId)
        if IsUseTwoPhone:
            self.driver2.quit()
        #filename = self.caseName + self.desired_caps['deviceName']+common.get_data()
        #adbShell.exit_gt(self.desired_caps['appPackage'], self.desired_caps['deviceName'], filename)
        #adbShell.copyfile(GTPath + filename, GT_Log_Path, self.driverId)
        # if IsUseTwoPhone:
        #     self.driver2.quit()
        #     filename2 = self.caseName + self.desired_caps2['deviceName'] + common.get_data()
        #     adbShell.exit_gt(self.desired_caps2['appPackage'], self.desired_caps['deviceName'], filename2)
        #     adbShell.copyfile(GTPath + filename2, GT_Log_Path, self.driverId2)

    def testIntoFeed(self):
        for i in range(2):
            adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/btn_negative', '取消弹窗', True)
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/tv_wording', '进入信息流'))
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/close_button', '返回首页'))
            log.info("testIntoFeed"+str(i))

    def testShareFeed(self):
        adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/btn_negative', '取消弹窗', True)
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/layout', '进入信息流'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_cover', '进入视频详情页'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/ll_share', '分享视频详情页'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/share_imo_friend', '选择分享给好友'))
        self.assertTrue(adbShell.clickXpath(self.driver, '分享第一个好友', '//android.widget.ListView/android.view.ViewGroup[1]/android.widget.RelativeLayout[1]'))
        adbShell.getElementText(self.driver, 'xpath', '分享好友名称', '//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.ListView[1]/android.view.ViewGroup[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView[1]')
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/ll_scene', '确定分享给该好友'))
        self.assertTrue(adbShell.clickXpath(self.driver2, '点击聊天窗口', '//android.widget.ListView[@resource-id=\"com.imo.android.imoimalpha:id/chats_list\"]/android.widget.LinearLayout[1]'))
        self.assertTrue(adbShell.clickID(self.driver2, 'com.imo.android.imoimalpha:id/tv_desc', '点击视频卡片'))
        time.sleep(5)



if __name__ == "__main__":

    #构造测试集
    suite = unittest.TestSuite()
    suite.addTest(FeedTest("testShareFeed"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)



