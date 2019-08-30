
# encoding: utf-8
import subprocess
from utils.logger import MyLogger
import logging
import time
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction
log = MyLogger(logging.DEBUG, logging.DEBUG)


def runCmd(cmd):
  res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  sout ,serr = res.communicate()
  time.sleep(2)
  return res.returncode, sout.decode("utf-8"), serr, res.pid


def getDeviceID():
    adb_com = 'adb devices'
    result = runCmd(adb_com)
    output = result[1]
    device_id = output.split()[4]
    return device_id


def open_gt(pkgName, deviceID):
    log.info("设备开启GT数据采集")
    try:
        gt_open = 'adb -s '+deviceID +' shell am start -W -n com.tencent.wstt.gt/com.tencent.wstt.gt.activity.GTMainActivity'
        gt_start = 'adb -s '+deviceID + ' shell am broadcast -a com.tencent.wstt.gt.baseCommand.startTest --es pkgName '+pkgName
        gt_CPU = 'adb -s '+deviceID + ' shell am broadcast -a com.tencent.wstt.gt.baseCommand.sampleData --ei cpu 1'
        gt_PSS = 'adb -s '+deviceID + ' shell am broadcast -a com.tencent.wstt.gt.baseCommand.sampleData --ei pss 1 '
        gt_NET = 'adb -s '+deviceID + ' shell am broadcast -a com.tencent.wstt.gt.baseCommand.sampleData --ei net 1'
        gt_Men = 'adb -s '+deviceID + ' shell dumpsys meminfo ' + pkgName
        runCmd(gt_start)
        runCmd(gt_open)
        runCmd(gt_CPU)
        runCmd(gt_PSS)
        runCmd(gt_NET)
        runCmd(gt_Men)
        time.sleep(8)
        log.info('设置GT悬浮窗')
    except Exception as ex:
        print(ex.__traceback__())


def exit_gt(pkgName, deviceID, fileName='test'):
    try:
        log.info('结束采集并保存，同时删除数据记录')
        gt_saveFile = 'adb -s ' + deviceID+" shell am broadcast -a com.tencent.wstt.gt.baseCommand.endTest --es saveFolderName '"+fileName +"'"
        gt_exit = 'adb -s ' + deviceID+' shell am broadcast -a com.tencent.wstt.gt.baseCommand.exitGT'
        runCmd(gt_saveFile)
        runCmd(gt_exit)
        time.sleep(8)
        log.info('设置GT悬浮窗')
    except Exception as ex:
        log.error(ex)

def copyfile(sd_path, pc_path,deviceID):
    # hh: mm:ss.000  excel获取毫秒时间，设置格式
    print(deviceID)
    adbCom = 'adb -s  ' + deviceID + " pull " + sd_path + " " + pc_path
    print(adbCom)
    runCmd(adbCom)
    log.info("拷贝数据成功！")


def clickID(driver, element_id, msg,skip=False):
    if isElement(driver, "id", element_id, msg, skip):
        driver.find_element_by_id(element_id).click()
        log.info('点击元素'+'----'+msg)
        time.sleep(5)
        return True
    else:
        log.error('点击元素失败，没有该元素' +element_id + '----' + msg)
        return False


def clickXpath(driver, msg, element_xpath, skip=False):
    if isElement(driver, "xpath", element_xpath, msg, skip):
        driver.find_element_by_xpath(element_xpath).click()
        log.info('点击元素' + '----' + msg)
        return True
    else:
        log.error('点击元素失败，没有该元素'+element_xpath + '----' + msg)
        return False


def getElementText(driver, type, msg, exlement):
    if type == 'xpath':
        element = driver.find_element_by_xpath(exlement)
    elif type == 'id':
        element = driver.find_element_by_id(exlement)
    text = element.get_attribute("text")
    log.info(msg+'------->'+text)
    return text


def isElement(driver, identifyBy, c, msg, skip = False):
    '''
    Determine whether elements exist
    Usage:
    isElement(By.XPATH,"//a")
    '''
    flag=False
    i=0
    if skip == True:
        i = 2
    while flag == False and i <= 2:
        try:
            time.sleep(10)
            if identifyBy == "id":
                driver.find_element_by_id(c)
            elif identifyBy == "xpath":
                driver.find_element_by_xpath(c)
            elif identifyBy == "class":
                driver.find_element_by_class_name(c)
            elif identifyBy == "link text":
                driver.find_element_by_link_text(c)
            elif identifyBy == "partial link text":
                driver.find_element_by_partial_link_text(c)
            elif identifyBy == "name":
                driver.find_element_by_name(c)
            elif identifyBy == "tag name":
                driver.find_element_by_tag_name(c)
            elif identifyBy == "css selector":
                driver.find_element_by_css_selector(c)
            flag = True
        except NoSuchElementException as ex:
            i = i+1
            log.error(msg+str(ex))
            # common = 'adb '
            flag = False
    return flag


def getSize(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)

def swipLeft(driver, msg ,duration = 1000):
    location = getSize(driver)
    x1 = int(location[0]*0.8)
    y1 = int(location[1]*0.5)
    x2 = int(location[0]*0.2)
    # driver.swipe(start=x1, starty=y1, endx=x2, endy=y1, duration=1000)
    # time.sleep(10)
    driver.swipe(x1, y1, x2, y1, 400)
    time.sleep(3)
    # driver.execute_script('mobile: shell', {
    #     'command': 'echo',
    #     'args': ['swipe', x1, y1, x2, y1, duration],
    #     'includeStderr': True,
    #     'timeout': 5000
    # })

    log.info("左滑坐标：("+str(x1)+'，'+str(y1)+')--->('+str(x2)+","+str(y1)+')')
    # #TouchAction(driver).press(x=x1, y=y1).wait(500).move_to(x=x2, y=y1).release().perform()
    # TouchAction(driver).press(x=1100, y=1250).wait(500).move_to(x=100, y=1250).release().perform()

#屏幕向右滑动
# def swipRight(driver,time='1000'):
#     location=getSize()
#     x1=int(location[0]*0.05)
#     y1=int(location[1]*0.5)
#     x2=int(location[0]*0.75)
#     driver.swipe(x1, y1, x2, y1, time)


if __name__ == "__main__":
    print(getDeviceID())
