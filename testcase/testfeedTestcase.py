
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

log = MyLogger(logging.DEBUG, logging.DEBUG)

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AndroidFeedTest(unittest.TestCase):
    caseName = ''

    @classmethod
    def setUpClass(cls):
        cls.driverId = 'HBSBB18818504562'
        cls.desired_caps = common.read_cofig('driver', cls.driverId)
        cls.driver = common.getDriver(cls.desired_caps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def testJudgeTitle(self):
        title = adbShell.getElementText(self.driver, 'id', '获取信息流标题', 'com.imo.android.imoimalpha:id/tv_title')
        self.assertEqual('Likee Videos', title)

    def testShareFeed(self):
        self.assertTrue(
            adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/layout_bottom_feeds_entrance', '进入信息流页面'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_cover', '点击视频', True))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/ll_share', '点击分享'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_share_icon', '选择分享给imo好友'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/icon', '选择第一个好友'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha:id/ll_scene', '点击发送'))
        self.assertTrue(adbShell.clickID(self.driver, 'com.imo.android.imoimalpha.Trending:id/iv_close', '点击返回，退出视频详情'))




if __name__ == "__main__":

    #构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(AndroidFeedTest("testJudgeTitle"))
    # suite.addTest(AndroidFeedTest("testShareFeed"))
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    suite = unittest.TestSuite()
    suite.addTest(AndroidFeedTest("testJudgeTitle"))
    suite.addTest(AndroidFeedTest("testShareFeed"))
    runner = unittest.TextTestRunner()
    report_path = PATH + "/report/" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()) + '.html'
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title="自动化测试unittest测试框架报告",
                                           description="用例执行情况：")
    runner.run(suite)
    fp.close()


