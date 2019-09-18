# coding: utf-8
import subprocess
import time
from apscheduler.schedulers.blocking import BlockingScheduler


class Monitor:
    """
    总的cpu时间totalCpuTime = user + nice + system + idle + iowait + irq + softirq + stealstolen +guest
    命令：adb shell cat /proc/stat 第一行即可
    进程的总Cpu时间processCpuTime = utime + stime + cutime + cstime
    命令:adb shell cat /proc/进程id/stat | awk '{print $14,$15,$16,$17}'
    计算该进程的cpu使用率pcpu = 100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1)

    pid 进程号
    utime 该任务在用户态运行的时间，单位为jiffies

    stime 该任务在核心态运行的时间，单位为jiffies

    cutime 所有已死线程在用户态运行的时间，单位为jiffies

    cstime 所有已死在核心态运行的时间，单位为jiffies
    """

    def __init__(self, udid, packageName):
        self.udid = udid
        self.packageName = packageName
        self.o_cpu = 0.0
        self.o_acpu = 0.0
        self.pid = self.getPid()
        self.uid = self.getUid()
        self.oldData = None
        self.rx_begin = 0
        self.tx_begin = 0

    def runCmd(self, cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sout, serr = res.communicate()
        time.sleep(2)
        return res.returncode, sout.decode('utf-8'), serr, res.pid

    def getPid(self):
        common = "adb -s " + self.udid + " shell \"ps |grep '" + self.packageName +"' \""
        result = self.runCmd(common)
        code = result[1].split()
        self.pid = code[1]
        return code[1]

    def getProcessCpuAction(self):
        cpuPath = "adb -s " + self.udid + " shell cat /proc/" + self.pid + "/stat"
        result = self.runCmd(cpuPath)
        if result[1]=='' or result[1]==None:
            return False
        cpuMess = result[1].split(" ")
        cupResult = []
        cupResult.append(cpuMess[1])
        cupResult.append(cpuMess[13])
        cupResult.append(cpuMess[14])
        cupResult.append(cpuMess[15])
        cupResult.append(cpuMess[16])
        return cupResult

    def getCpuAction(self):
        cpuPath = "adb -s " + self.udid + " shell cat /proc/stat"
        result = self.runCmd(cpuPath)
        rows = result[1].strip('\r').split("\n")
        columns = rows[0].split()
        return columns

    def getCpuPressent(self):
        processTimeList = self.getProcessCpuAction()
        if not processTimeList:
            return
        processTime = float(processTimeList[1]) + float(processTimeList[2])+float(processTimeList[3])+float(processTimeList[4])
        totalCpuTimeList = self.getCpuAction()
        totalCpuTime = 0
        for i in range(1, len(totalCpuTimeList)):
            totalCpuTime =float(totalCpuTimeList[i])+float(totalCpuTime)
        cpu = round((processTime - self.o_cpu)*100 / (totalCpuTime - self.o_acpu), 2)
        self.o_acpu = totalCpuTime
        self.o_cpu = processTime
        return str(cpu)+'%'


    def getMemory(self):
        adb_memory = "adb -s %s shell dumpsys meminfo %s" % (self.udid, self.packageName)
        result = self.runCmd(adb_memory)
        memory = result[1].splitlines()
        total_index = result[1].find("TOTAL")
        Graphics_index = result[1].find("Graphics")
        try:
            memoryDic={
                "Native_Heap": memory[7].split()[2],
                "Dalvik_Heap": memory[8].split()[2],
                "Native_Heap_Heap_Free": memory[7].split()[8],
                "Dalvik_Heap_Heap_Free": memory[8].split()[8],
                "Graphics": result[1][Graphics_index+10:Graphics_index+20].strip(),
                "TOTAL":  result[1][total_index+6:total_index+16].strip()
            }
            return memoryDic
        except Exception as e:
            print(e)
            print(memory)

    def getUid(self):
        adb_uid = "adb -s %s shell cat /proc/%s/status" % (self.udid, self.pid)
        result = self.runCmd(adb_uid)
        index = result[1].find("Uid:")
        uid = result[1][index+5:index+10].strip()
        return uid

    def getCommondLine(self, command):
        result = self.runCmd(command)
        return result[1].splitlines()

    def getNetDate(self):
        """
        adb_net：获取流量的命令
        adb_net的流量的第六列是接收数据
        adb_net的数据的第八列是发送数据(bytes)
        获取数据的单位为byte，byte需要转化为KB, 1KB = 1024 Bytes
        :return:
        """
        adb_net = "adb -s %s shell \"cat /proc/net/xt_qtaguid/stats | grep %s \" " % (self.udid, self.uid)
        netLine = self.getCommondLine(adb_net)
        rxBytes = 0
        txBytes = 0

        for i in range(len(netLine)):

            line = netLine[i].split()
            if len(line) > 8:
                rxBytes = float(line[5]) + rxBytes
                txBytes = float(line[7]) + txBytes

        if self.rx_begin == 0:
            self.rx_begin = rxBytes
            self.tx_begin = txBytes

        net = { "rxKb": ((rxBytes - self.rx_begin)/1024.0), "txKb": ((txBytes - self.tx_begin)/1024.0), "time": time.time()}
        return net

    def getNetDataUsed(self):
        """
        nowData：getNetDate返回的time单位为毫秒
        :return:
        """

        if self.oldData == None:
            self.oldData = {"time": time.time(), "rxKb": 0, "txKb": 0}
        nowData = self.getNetDate()
        millisecond = nowData["time"] - self.oldData["time"]
        rxSpeed = round((nowData['rxKb'] - self.oldData['rxKb']) / millisecond, 4)
        txSpeed = round((nowData['txKb'] - self.oldData['txKb']) / millisecond, 4)
        # rxSpeed = round(rxSpeed * 1000, 4)
        # txSpeed = round(txSpeed * 1000, 4)

        Net = {"rxKb": nowData["rxKb"], "txKb": nowData['txKb'], "rxSpeed": rxSpeed, "txSpeed": txSpeed}
        self.oldData = nowData

        return Net

    def getMonitor(self):

        print(self.getMemory())
        print(self.getNetDate())
        #self.getCpuPressent()
        print("cpu:"+self.getCpuPressent())
        data = {"cpu": self.getCpuPressent()}
        return data


if __name__ == '__main__':
    # monitor = Monitor("03157df3ea406008", 'com.imo.android.imoimalpha')
    # for i in range(50):
    #     monitor.getMonitor()
    print("ssss")

