
# encoding: utf-8
import subprocess
from utils.logger import MyLogger
import logging
import time
from selenium.common.exceptions import NoSuchElementException

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



def clickID(driver, element_id,msg,skip=False):
    if isElement(driver,"id", element_id, msg, skip):
        driver.find_element_by_id(element_id).click()
        time.sleep(5)
        log.info('点击元素'+'----'+msg)
        return True
    else:
        log.error('点击元素失败，没有该元素' + '----' + msg)
        return False


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
    while flag == False and i <= 2 :
        try:
            time.sleep(5)
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
            flag = False
    return flag


if __name__ == "__main__":
    print(getDeviceID())
