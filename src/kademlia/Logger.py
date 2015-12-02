import logging

class Logger(object):
    """Logger

    Create a Logger object.
    """
    def __init__(self, config):
        """Logger

        Args:
            config: a logger config object
        """
        self.config = config

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.config["level"])
        return logger
