# coding=gbk
import logging
import time
import os
import colorlog

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

class MyLogger:

    def __init__(self, clevel=logging.DEBUG, Flevel=logging.DEBUG):

        PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        timestr = time.strftime("%Y%m%d", time.localtime())
        filePath = PATH+"\\log\\"+timestr+".log"

        self.logger = logging.getLogger(filePath)
        self.logger.setLevel(logging.DEBUG)
        format = '[%(asctime)s] - %(levelname)s - %(message)s'
        cmt = logging.Formatter(format, '%Y/%m/%d %H:%M:%S')
        fmt = colorlog.ColoredFormatter(
            '%(log_color)s'+format, '%Y/%m/%d %H:%M:%S',
            log_colors=log_colors_config)

        if not self.logger.handlers:
            # �����ļ���־����־��Ϣ����������ļ�
            fh = logging.FileHandler(filePath)
            fh.setFormatter(cmt)
            fh.setLevel(Flevel)
            self.logger.addHandler(fh)
            # ����CMD��־�����ʽ������־��Ϣ�����sys.stdout, sys.stderr �������ļ�����
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            sh.setLevel(clevel)
            self.logger.addHandler(sh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    log = MyLogger(logging.DEBUG, logging.DEBUG)
    log.debug('һ��debug��Ϣ')
    log.info('һ��info��Ϣ')
    log.warning('һ��warning��Ϣ')
    log.error('һ��error��Ϣ')
    log.critical('һ������critical��Ϣ')