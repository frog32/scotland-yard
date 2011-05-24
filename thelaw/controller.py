import random
import logging
import networkx as nx

class SimpleController(object):
    mr_x_position = None
    logger = None

    def __init__(self, graph, mr_x, polices, move_cls, logger):
        self.graph = graph
        self.mr_x = mr_x
        self.polices = polices
        self.move_cls = move_cls
        self.logger = logger

    def draw(self, round, who):
        choices = self.graph.neighbors(who.get_position())
        r = random.randint(0, len(choices)-1)
        target = choices[r]
        move_type = self.graph[who.get_position()][target][0]['ticket']
        if who.tickets_cab==1:
            who.tickets_cab = 2
        return self.move_cls(target, move_type)
  