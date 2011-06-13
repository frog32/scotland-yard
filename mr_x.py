import random
import logging
import networkx as nx
import copy


class MrX(object):
    graph = None
    logger = None
    move_cls = None
    status_count = 0
    def __init__(self, graph, mr_x, polices, move_cls, logger):
        MrX.graph = graph
        self.mr_x = mr_x
        self.polices = polices
        MrX.move_cls = move_cls
        MrX.logger = logger
        self.status = Status(PlayerLight(self.mr_x.get_position()),list(PlayerLight(police.get_position()) for police in self.polices),-1)
        self.status.build_levels(6)
        MrX.logger.info('Mr.X init complete. created %d status and avoided %d' % (Status.count_created, Status.count_avoided))
        # self.status.recursive_dump()
        
    def draw(self, round, who):
        MrX.logger.info('Start Move from %s' % who.get_position())
        self.status = self.status.find_current_child(self.mr_x, self.polices)
        target, ticket = self.status.get_securest_next_move()
        MrX.logger.info('Try moving to %s by %s' % (target, ticket))
        return self.move_cls(target, ticket)

class Status(object):
    count_created = 0 # object counter
    count_avoided = 0
    
    def __init__(self, mr_x, polices, next_player):
        """
        mr_x        copy of mr_x player
        polices     copy of polices
        next_player next player, -1 = mr_x, all others are indexes of the police array
        """
        Status.count_created += 1
        self.choices = []
        self.mr_x = mr_x
        self.polices = polices
        self.next_player = next_player
        self.distance = self.calculate_min_distance()
        MrX.status_count +=1
            
    def calculate_min_distance(self):
        """returns the minimum distance from mrx to any police"""
        distances = []
        for police in self.polices:
            distances.append(nx.shortest_path_length(MrX.graph, self.mr_x.position, police.position))
            MrX.logger.debug('minimum distance to police %d' % min(distances))
        return min(distances)
    
    def build_levels(self, level_count):
        """build n levels recursive"""
        if not len(self.choices) and level_count >= 1:
            self.build_next_level()
        for choice in self.choices:
            choice.build_levels(level_count-1)
    
    def build_next_level(self):
        """build only the next level"""
        if self.next_player == -1:
            next = self.mr_x
        else:
            next = self.polices[self.next_player]
        neighbors = MrX.graph.neighbors(next.position)
        for target in neighbors:
            # check if we realy need this status
            obsolete_status = False
            for police in self.polices:
                if target == police.position:
                    obsolete_status = True
                    break
            if obsolete_status:
                Status.count_avoided += 1
                continue
            ticket = MrX.graph[next.position][target][0]['ticket']
            status = Status(copy.copy(self.mr_x), copy.deepcopy(self.polices),(self.next_player+2)%(len(self.polices)+1)-1)
            if self.next_player == -1:
                status.mr_x.position = target
                status.mr_x.last_ticket = ticket
            else:
                status.polices[self.next_player].position = target
                status.polices[self.next_player].last_ticket = ticket
            self.choices.append(status)

    def __cmp__(self, other):
        if not isinstance(other, Status):
            raise
        distance_diff = self.distance - other.distance
        # if min_distance != 0:
        return distance_diff
    
    def get_securest_next_move(self):
        if len(self.choices) == 0:
            self.build_levels(6)
        self.choices.sort()
        return self.choices[0].get_mr_x_move()
    
    def get_mr_x_move(self):
        return self.mr_x.position, self.mr_x.last_ticket
    
    def dump(self):
        print "**************************"
        print "  player      position"
        print "%s mrx         %d" % ('*' if self.next_player== -1 else ' ',self.mr_x.position)
        for i, police in enumerate(self.polices):
            print "%s police%d     %d" % ('*' if self.next_player == i else ' ',i+1, police.position)
    
    def recursive_dump(self, max_levels=100, level=0):
        print max_levels, level
        print "** level %d ***" % level
        self.dump()
        if max_levels <= 1:
            return
        for status in self.choices:
            status.recursive_dump(max_levels-1, level+1)
    
    def find_current_child(self,mr_x, polices):
        if self.mr_x.get_position() == mr_x.get_position():
            match = True
            for i in range(len(self.polices)):
                if self.polices[i].get_position() != polices[i].get_position():
                    match = False
                    break
            if match:
                return self
        for status in self.choices:
            if self.next_player == -1:
                if status.mr_x.get_position() == mr_x.get_position():
                    return status.find_current_child(mr_x, polices)
            else:
                if status.polices[self.next_player].get_position() == polices[self.next_player].get_position():
                    return status.find_current_child(mr_x, polices)
        MrX.logger.error("didn't find current state")

class PlayerLight(object):
    def __init__(self, start_position, last_ticket=''):
        self.position = start_position
        self.last_ticket = last_ticket
    
    def get_position(self):
        return self.position
    
