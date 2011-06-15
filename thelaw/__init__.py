import logging

__author__ = 'Tarik'

def init_logger(self, level):
    self.logger = logging.getLogger('police.Police')
    self.logger.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s:%(name)s: %(message)s")
    ch.setFormatter(formatter)
    self.logger.addHandler(ch)
  