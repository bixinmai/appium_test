
# encoding: utf-8
import logging
from utils.logger import MyLogger
from utils import common
from utils import adbShell
import os
import unittest
from utils.jarfile import Jar
import time
import HTMLTestRunner
from appium.webdriver.common.touch_action import TouchAction


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GTPath = "/sdcard/GT/GW/com.imo.android.imoimalpha/unknow/"
GT_Log_Path = PATH+'\\'+'GT\\'
#GT_Log_Path = PATH+'/'+'GT/'
IsUseTwoPhone = True
jar_path = 'F:\\test-gt\\jar\\Monitor.jar'
monitor_package_name = 'sg.bigo.dump.RunMonitor'
packName = "com.imo.android.imoimalpha"
log = MyLogger(logging.DEBUG, logging.DEBUG)

class AndroidFeedTest(unittest.TestCase):
    caseName = ''

    @classmethod
    def setUpClass(cls):
        cls.driverId = 'SKC6IVAUOZZL8DHA'
        cls.desired_caps = common.read_cofig('driver', cls.driverId)
        cls.driver = common.getDriver(cls.desired_caps)
        # 用Monitor检测性能
        cls.monitorJar = Jar()
        cls.monitor = cls.monitorJar.StartMonitor(monitor_package_name, jar_path, cls.driverId, packName)

    # def setUp(self):
    #     self.driver = common.getDriver(self.desired_caps)

    # def tearDown(self):
    #     self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.monitorJar.stopMonitor(cls.monitor, cls.driverId)


    def testIntoDetail(self):
        log.info("反复进入视频详情页")
        self.assertTrue(
            adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/layout_bottom_feeds_entrance', '进入信息流页面'))
        for i in range(200):
            log.info('弟'+str(i)+"次进入详情页")
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_cover', '点击视频', True))
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_close', '点击返回，退出视频详情'))

    def testReturnLeft(self):
        log.info("测试用例----反复左滑，再反复返回")
        self.assertTrue(
            adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/layout_bottom_feeds_entrance', '进入信息流页面'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_cover', '点击视频'))
        for i in range(2):
            log.info("滑动进入个人页第"+str(i)+"次")
            adbShell.swipLeft(self.driver, '视频详情页左滑')
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_cover', '点击个人页post的第一个视频'))
        for i in range(2):
            log.info("返回上一级" + str(i) + "次")
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_close', '点击视频详情页返回'))
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_back', '点击个人页返回'))

    def testIntoFeed(self):
        log.info("测试用例----反复进入信息流")
        time.sleep(5)
        for i in range(200):
            log.info("进入信息流第" + str(i) + "次")
            # adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/btn_negative', '取消弹窗', True)
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/tv_wording', '进入信息流'))
            self.assertTrue(
                adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_close', '点击视频详情页返回'))
            self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/close_button', '返回首页'))
            log.info("testIntoFeed"+str(i))

    def deleteIntroduceFriend(self):
        log.info("测试用例----反复删除推荐的人")
        for i in range(200):
            self.assertTrue(
                adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_delete', '删除推荐的人'))

    def deleteFriend(self):
        log.info("测试用例----反复删除关注的人")
        for i in range(200):
            self.assertTrue(
                adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_icon_center', '删除关注的人'))
            self.assertTrue(
                adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/tv_un_follow', '删除关注的人'))



if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(AndroidFeedTest("deleteFriend"))
    runner = unittest.TextTestRunner()
    report_path = PATH+"/report/" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()) + '.html'
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title="自动化测试unittest测试框架报告",
                                           description="用例执行情况：")
    runner.run(suite)
    fp.close()


