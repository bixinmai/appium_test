# coding=utf-8
import os
packName = "com.imo.android.imoimalpha"
GTPath = "/sdcard/GT/GW/com.imo.android.imoimalpha/unknow/"

CurPath =os.path.abspath(os.path.dirname(__file__))

RootPath = os.path.dirname(CurPath)
PerformanceDataPath = os.path.join(RootPath, 'PerformanceData')

if __name__=='__main__':
    print(RootPath)