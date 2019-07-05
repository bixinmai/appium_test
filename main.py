#coding:utf-8
import unittest
import HTMLTestRunner
import importlib, sys
importlib.reload(sys)
import os
import time


#待执行用例的目录
def allcase():
    #写路径即可
    #case_dir="/testcase"
    case_path=os.path.join(os.getcwd(), "testcase")
    testcase=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(case_path,
                                                 pattern='test*.py',
                                                 top_level_dir=None)
    #discover方法筛选出来的用例，循环添加到测试套件中
    #print(discover)
    for test_suite in discover:
        for test_case in test_suite:
            #添加用例到testcase
            print(test_case)
            testcase.addTest(test_case)

    return testcase
if __name__=="__main__":
    runner = unittest.TextTestRunner()
    runner.run(allcase())

    report_path = "report/"+time.strftime("%Y%m%d", time.localtime())+'.html'
    fp = open(report_path, "w", encoding='utf-8')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                         title="自动化测试unittest测试框架报告",
                                         description="用例执行情况：")
    runner.run(allcase())
    fp.close()
