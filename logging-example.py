import logging
import logging.config

# configure 
logging.config.fileConfig('logging-example.conf')

# create root logger, output to console
root_logger = logging.getLogger()

# create file logger, output to log file
file_logger = logging.getLogger('fileExample')

# log into root logger only
root_logger.debug('debug root')
root_logger.info('info root')
root_logger.warn('warn root')
root_logger.error('error root')
root_logger.critical('critical root')


# log to a file, propaget to root logger
file_logger.debug('debug file')
file_logger.info('info file')
file_logger.warn('warn file')
file_logger.error('error file')
file_logger.critical('critical file')
