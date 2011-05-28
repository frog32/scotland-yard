import random
import logging
import police
import ConfigParser

class Police(object):

    logger = None
    controller = None

    def __init__(self, graph, mr_x, polices, move_cls, logger):
        self.logger = logger
        config = ConfigParser.ConfigParser()
        config.read('police.cfg')
        if config.get("Police", "controller_module") and config.get("Police", "controller_class"):
            classlist = __import__(config.get("Police", "controller_module"), fromlist=[config.get("Police", "controller_class")])
            controller_class = getattr(classlist, config.get("Police", "controller_class"))
            self.controller = controller_class(graph, mr_x, polices, move_cls, logger)
        else:
            self.controller = SimpleController(graph, mr_x, polices, move_cls, logger)

    def draw(self, round, who):
        self.logger.debug('draw called in ', round, '. round for officer: ', who)
        return self.controller.draw(round, who)
        