# coding=utf-8
from utils import config as gl
from utils.MonitorUnit import Monitor
import threading
import os
import csv
import time
class GetPerformance():

    def __init__(self):
        self.monitor_flag = True

    def run_monitor(self):
        curTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        dir =os.path.join(gl.PerformanceDataPath, curTime)
        if not os.path.exists(dir):
            os.mkdir(dir)
        try:
            cpuName = os.path.join(dir, "cpu_"+curTime) + '.csv'
            netName = os.path.join(dir, "cpu_"+curTime) + '.csv'
            menName = os.path.join(dir, "cpu_"+curTime) + '.csv'
            cpuFile = open(cpuName, 'w', newline='') #创建csv文件
            cpuWrite = csv.writer(cpuFile)
            cpuWrite.writerow(["time", "cpu"])     #写入列的名称
            # netName = open(cpuName, 'a')
            # menName = open(cpuName, 'a')
            # cpuWrite.writerow(["11:08", "0.8%"])
            # cpuWrite.writerow(["11:10", "1.8%"])
            while self.monitor_flag:
                monitor = Monitor("UYT7N17A31005712", 'com.imo.android.imoimalpha')
                Data = monitor.getMonitor()
                nowtime = time.strftime("%H-%M-%S", time.localtime())
                cpuWrite.writerow([nowtime, Data["cpu"]])
            cpuFile.close()
        except Exception as e:
            print(e)
            cpuFile.close()
        # menName.close()
        # while self.monitor_flag:
        #     monitor = Monitor("UYT7N17A31005712", 'com.imo.android.imoimalpha')
        #     monitor.getMonitor()

    def stop(self):
        self.monitor_flag =False


if __name__=='__main__':
    monitor = GetPerformance()
    monitor_thread = threading.Thread(target=monitor.run_monitor)
    monitor_thread.start()
    # time.sleep(10000)
    # monitor_thread.stop()




