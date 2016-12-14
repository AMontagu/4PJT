"""

Helpers functions for python logging. See : https://docs.python.org/3/library/logging.html

"""

import inspect
import json
import logging

import apipython.globalInfo as globalInfo

logger = None
logFormatter = None
ch = None
stdOutIsEnable = False


def initializeLog(loggerName, fileName, enableStdOut=False, level=10):
	"""
	Initialize the log system

	:param loggerName: The name of the logger object for multi module use if needed
	:param fileName: the name of the file were the log are stored in the directory for this (resources/log/)
	:param enableStdOut: True if we print in the console (non daemon process)
	:param level: CRITICAL	50, ERROR	40, WARNING	 30, INFO	 20, DEBUG	10, NOTSET	0
	:return:
	"""
	global logFormatter
	logFormatter = logging.Formatter("%(asctime)s (%(created)f) [%(threadName)-s] [%(levelname)s] |  %(message)s")

	global logger
	logger = logging.getLogger(loggerName)

	logger.setLevel(level)
	try:
		fh = logging.FileHandler(globalInfo.getHeaseRepertory() + "resources/log/" + str(fileName))
	except PermissionError:
		fh = logging.FileHandler("/tmp/" + str(fileName))

	fh.setFormatter(logFormatter)
	logger.addHandler(fh)

	global stdOutIsEnable

	if enableStdOut:
		global ch
		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setFormatter(logFormatter)
		logger.addHandler(ch)
		stdOutIsEnable = True
	else:
		stdOutIsEnable = False

	"""logger.debug('debug message')
	logger.info('info message')
	logger.warn('warn message')
	logger.error('error message')
	logger.critical('critical message')"""


def logSetLevel(level):
	global logger
	logger.setLevel(level)


def logSetStdOut(enable):
	global logger
	global ch
	global stdOutIsEnable
	if enable and not stdOutIsEnable:
		ch = logging.StreamHandler()
		ch.setFormatter(logFormatter)
		logger.addHandler(ch)
		stdOutIsEnable = True
	elif stdOutIsEnable:
		logger.removeHandler(ch)
		stdOutIsEnable = False

def checkMessage(message):
	if isinstance(message, str):
		return message
	else:
		return json.dumps(message)

def LOGDEBUG(message):
	message = checkMessage(message)
	global logger
	if logger != "" and logger is not None:
		(frame, filename, line_number,
		 function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		log = filename + ":" + str(line_number) + " | " + message
		logger.debug(log)
	else:
		print("logger not initialized")

def LOGINFO(message):
	message = checkMessage(message)
	global logger
	if logger != "" and logger is not None:
		(frame, filename, line_number,
		 function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		log = filename + ":" + str(line_number) + " | " + message
		logger.info(log)
	else:
		print("logger not initialized")

def LOGWARN(message):
	message = checkMessage(message)
	global logger
	if logger != "" and logger is not None:
		(frame, filename, line_number,
		 function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		log = filename + ":" + str(line_number) + " | " + message
		logger.warn(log)
	else:
		print("logger not initialized")

def LOGERROR(message):
	message = checkMessage(message)
	global logger
	if logger != "" and logger is not None:
		(frame, filename, line_number,
		 function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		log = filename + ":" + str(line_number) + " | " + message
		logger.error(log)
	else:
		print("logger not initialized")

def LOGCRITICAL(message):
	message = checkMessage(message)
	global logger
	if logger != "" and logger is not None:
		(frame, filename, line_number,
		 function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
		log = filename + ":" + str(line_number) + " | " + message
		logger.critical(log)
	else:
		print("logger not initialized")
