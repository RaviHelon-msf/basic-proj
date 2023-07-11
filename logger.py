import logging
import logging.config

logging.config.fileConfig('logging.conf')

root = logging.getLogger()
test = logging.getLogger('test')


if __name__ == '__main__':
    test.debug("debug")
    test.info("info")
    test.warning("warning")
    test.error("error")
    test.critical("critical")