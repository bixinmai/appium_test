# encoding: utf-8
import os
# PATH = os.path.dirname(os.path.abspath(__file__))
# GTPath = "/sdcard/GT/GW/com.imo.android.imoimalpha/2019.1.56/test/"
# Path_T = PATH+'\\'+'GT'
# log = MyLogger(PATH+'//log', logging.DEBUG, logging.DEBUG)
PATH = os.path.dirname(os.path.abspath(__file__))
Path_T = os.path.join(PATH, 'GT')

if __name__ == '__main__':
    print(Path_T)