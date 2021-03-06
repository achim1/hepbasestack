"""
A logger with customizable loglevel at runtime. The loglevel can be set via the 
global `LOGLEVEL` variable. 
"""

import logging
import inspect
import os
import sys

LOGFORMAT = '%(levelname)s:%(message)s:%(module)s:%(funcName)s:%(lineno)d'
#LOGFORMAT = '%(levelname)s:%(message)s'
LOGLEVEL  = 30
alertstring = lambda x :  "\033[0;31m" + x + "\033[00m"

logging.captureWarnings(True)

def get_logger(loglevel):
    """
    A logger from python logging on steroids.

    Args:
        loglevel (int): 10 = DEBUG, 20 = INFO, 30 = WARNING

    Returns:
        logging.Logger
    """

    def exception_handler(exctype, value, tb):
        logger.critical("Uncaught exception", exc_info=(exctype, value, tb))

    logger = logging.getLogger()
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    formatter = logging.Formatter(LOGFORMAT)
    ch.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(ch)
    #FIXME: this seems not to be necessary
    if len(logger.handlers) > 1:
        logger.handlers = [logger.handlers[1]]

    sys.excepthook = exception_handler
    return logger


class AbstractCustomLoggerType(type):
    """
    A modified logging.logger. Do not use directly, but as metaclass.
    Whenever the logger is called, HErmes.utils.logger.LOGLEVEL is queried
    to check for a change in the loglevel and a new logger instance is created
    accordingly. Python inspect is used to inspect the
    stack.
    """

    @staticmethod
    def __getattr__(item):
        logger = get_logger(LOGLEVEL)
        if len(logger.handlers) > 1:
            logger.handlers = [logger.handlers[1]]

        def wrapper(args):

            #for i in 0,1,2,3:
            #    frame = inspect.getouterframes(inspect.currentframe())[i]
            #    filename = frame[1]
            #    funcname = frame[2]
            #    lineno = frame[3]
            #    #print (i,filename, funcname, lineno)
            #    test = "{},{},{},{}".format(i, filename, funcname, lineno)
            #    print (test)
            #    del frame
            stack = 0
            fname = "wrapper"
            while fname == "wrapper":
                calframe = inspect.getouterframes(inspect.currentframe())[1 + stack]
                mname = os.path.split(calframe[1])[1].replace(".py","")
                lineno = calframe[2]
                fname = calframe[3]
                stack+=1
            #if "module" in fname:
            #    fname = "module"

            args += f":{mname}:{fname}:{lineno}"
            return getattr(logger, item)(args)

        return wrapper


class Logger(metaclass=AbstractCustomLoggerType):
    """
    A custom logger with loglevel changeable at runtime. To change the loglevel,
    set global LOGLEVEL variable in this namespace:
    10 = DEBUG, 20 = INFO, 30 = WARNING
    """
    pass


