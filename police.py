import random
import logging

class Police(object):
    
    def __init__(self, graph, mr_x, polices, move_cls):
        self.graph = graph
        self.mr_x = mr_x
        self.polices = polices
        self.move_cls = move_cls
    
    def init_logger(self, level):
        self.logger = logging.getLogger('mr_x.Police')
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s:%(name)s: %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def draw(self, round, who):
        choices = self.graph.neighbors(who.get_position())
        r = random.randint(0, len(choices)-1)
        target = choices[r]
        move_type = self.graph[who.get_position()][target][0]['ticket']
        return self.move_cls(target, move_type)
        