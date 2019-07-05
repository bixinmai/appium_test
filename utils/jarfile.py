# encoding: utf-8
import time
import jpype


class Jar:

    def StartMonitor(self, pack_name, jar_path, deviceId, packName):
        JDClass = self.openJvm(jar_path, pack_name)
        JDClass.startMonitor(deviceId, "", packName)
        return JDClass

    def stopMonitor(self, JDClass, deviceID):
        JDClass.stopMonitor(deviceID)
        self.shutdownJVM()

    def openJvm(self, jar_path, pack_name):
        # 获取系统的jvm路径
        jvm_path = jpype.getDefaultJVMPath()
        jpype.startJVM(jvm_path, "-ea", "-Djava.class.path="+jar_path, convertStrings=False)# 设置jvm路径，以启动java虚拟机
        JDClass = jpype.JClass(pack_name)
        return JDClass

    def shutdownJVM(self):
        jpype.shutdownJVM()
        # 关闭jvm虚拟机，当使用完 JVM 后，可以通过 jpype.shutdownJVM() 来关闭 JVM，该函数没有输入参数。当 python 程序退出时，JVM 会自动关闭。

if __name__=='__main__':
    jar_path = 'F:\\test-gt\\jar\\Monitor.jar'
    pack_name = 'sg.bigo.dump.RunMonitor'
    deviceId = "a22ec83d"
    packName = "com.imo.android.imoimalpha"
    monitorJar = Jar()
    monitor = Jar().StartMonitor(pack_name, jar_path, deviceId, packName)
    monitorJar.stopMonitor(monitor, deviceId)



