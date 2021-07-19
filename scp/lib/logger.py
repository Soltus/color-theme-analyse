# -*- coding=utf-8

# SCSD-PY001

# hi-windom/ColorThemeAnalyse

# https://gitee.com/hi-windom/color-theme-analyse

'''
# ---------------------------------
# 创建于    2021-7-20
# 更新于    2021-7-20 02:23:27
# ---------------------------------
# Need help ?  => 694357845@qq.com
# ---------------------------------
#  作者很懒，还没想好说些什么
# ---------------------------------
'''

################################################################
import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"

COLORS = {
    'WARNING': GREEN,
    'INFO': CYAN,
    'DEBUG': WHITE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
}
""" logger.debug('debug 信息 蓝色')
    logger.info('info 信息 白色')
    logger.warning('warning 信息 绿色')
    logger.error('error 信息 红色')
    logger.critical('critial 信息 橙色')  // alias for fatal error  """

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        message = str(record.msg)
        funcName = record.funcName
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            message_color = COLOR_SEQ % (30 + COLORS[levelname]) + message + RESET_SEQ
            funcName_color = COLOR_SEQ % (30 + COLORS[levelname]) + funcName + RESET_SEQ
            record.levelname = levelname_color
            record.msg = message_color
            record.funcName = funcName_color
        return logging.Formatter.format(self, record)


LOGFORMAT = "%(filename)s:%(lineno)d >>> [ %(levelname)s ]\t%(asctime)s    %(message)s\t%(name)s"
LOG_LEVEL = logging.DEBUG
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logging.root.setLevel(LOG_LEVEL)
log = logging.getLogger('logconfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

def myLogging(name):
    log = logging.getLogger(name)
    log.setLevel(LOG_LEVEL)
    log.addHandler(stream)
    return log
