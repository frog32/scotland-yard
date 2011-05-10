import random
import logging
import networkx as nx

class MrX(object):
    graph = None
    logger = None
    def __init__(self, graph, mr_x, polices, move_cls, logger):
        MrX.graph = graph
        self.mr_x = mr_x
        self.polices = polices
        self.move_cls = move_cls
        self.logger = logger
        
    def draw(self, round, who):
        choices = MrX.graph.neighbors(who.get_position())
        MrX.logger.debug('Start Move from %s' % who.get_position())
        MrX.logger.debug('choices =%s'% choices)
        police_positions = list(p.get_position() for p in self.polices)
        choices = list(Choice(who.get_position(), target, police_positions) for target in choices)
        choices.sort()
        choice = choices[-1]
        MrX.logger.debug('move to %s by %s' % (choice.target, choice.move_type))
        return self.move_cls(choice.target, choice.move_type)

class Choice(object):
    def __init__(self ,position , target, police_positions):
        self.target = target
        self.distances = []
        MrX.logger.debug('evaluating %s' % target)
        for police_position in police_positions:
            self.distances.append(nx.shortest_path_length(MrX.graph, target, police_position))
        self.min_distance = min(self.distances)
        MrX.logger.debug('minimum distance to police %d' % self.min_distance)
        # allways choose the first ticket
        self.move_type = MrX.graph[position][self.target][0]['ticket']
        
    def __cmp__(self, other):
        if not isinstance(other, Choice):
            raise
        min_distance_diff = self.min_distance - other.min_distance
        # if min_distance != 0:
        return min_distance_diff
