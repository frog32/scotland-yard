import exceptions
import networkx as nx
import random
import logging

VERBOSITY = 0

class Application(object):
    police_module, mr_x_module = None, None
    graph = None
    start_positions = []
    def __init__(self, police_module, mr_x_module, police_count=5, log_core=None, log_mrx=None, log_police=None):
        self.init_loggers(log_core, log_mrx, log_police)
        self.load_map()
        self.logger.debug('Created Map')
        self.polices = []
        position, positions = random_select(self.start_positions[:])
        self.x = Player(position, 'Mr X', True) # start position 
        self.x_pub = self.x.init_x(police_count)
        self.logger.debug('Created %s' % self.x)
        for i in range(police_count):
            position, positions = random_select(positions)
            police = Player(position, 'Police %s' % (i+1)) # startnode is i for testing purposes
            self.polices.append(police)
            self.logger.info('Created %s' % police)
        del positions
        self.players = [self.x] + self.polices
        self.mr_x_module = mr_x_module(self.graph, self.x, self.polices, Move, self.mr_x_logger)
        self.police_module = police_module(self.graph, self.x_pub, self.polices, Move, self.police_logger)
        # init gui
        self.round = 0
        self.active_player = len(self.players)
        # ready to start game
        self.logger.debug("init completed")
        
    def play(self):
        while True:
            self.play_round()
    
    def play_round(self):
        self.active_player += 1
        if self.active_player >= len(self.players):
            self.round += 1
            self.active_player = 0
            self.logger.info("round %s" % self.round)
            if self.round > 22:
                raise EndOfGame('Mr.X hat gewonnen.')
        player = self.players[self.active_player]
        if player.is_x:
            module = self.mr_x_module
        else:
            module = self.police_module
        move = module.draw(self.round,player)
        player.draw(move, self.graph)
        self.logger.info("%s went to %s by %s" % (player, move.target, move.ticket))
        if player.is_x:
            pass
        else:
            if player.get_position() == self.x.get_position():
                self.logger.info('Mr x geschnappt von %s'% player)
                raise EndOfGame('Police hat gewonnen.')
            self.x.add_ticket(move.ticket)
        
    def init_loggers(self, log_core, log_mrx, log_police):
        self.logger = logging.getLogger('start.Application')
        self.logger.setLevel(log_core)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s:%(name)s: %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        self.mr_x_logger = logging.getLogger('mr_x.MrX')
        self.mr_x_logger.setLevel(log_mrx)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s:%(name)s: %(message)s")
        ch.setFormatter(formatter)
        self.mr_x_logger.addHandler(ch)
        
        self.police_logger = logging.getLogger('mr_x.Police')
        self.police_logger.setLevel(log_police)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s:%(name)s: %(message)s")
        ch.setFormatter(formatter)
        self.police_logger.addHandler(ch)
        
        

    def load_map(self):
        self.start_positions = [13, 26, 29, 34, 50, 53, 91, 94, 103, 112, 117, 132, 138, 155, 174, 197, 198]
        self.graph = nx.MultiGraph()
        for edge in open('maps/kanten.txt'):
            bits = edge.replace('\n','').split(' ')
            self.graph.add_edge(int(bits[0]),int(bits[1]), attr_dict={'ticket':bits[2]})
            
class Move(object):
    TICKETS = ['cab', 'bus', 'underground', 'black']
    def __init__(self, target, ticket):
        self.target = target
        self.ticket = ticket
    
    def __repr__(self):
        return "Move to %s by %s" % (self.target, self.ticket)
    
    def clone_hidden(self):
        return Move(None ,self.ticket)

class PlayerGeneric(object):
    
    def __init__(self, name):
        self.tickets_cab = 10
        self.tickets_bus = 8
        self.tickets_underground = 4
        self.tickets_black = 0
        self.tickets_double = 0
        self.moves = []
        self.name = name
        
    
    def __repr__(self):
        return self.name

class PlayerX(PlayerGeneric):
    VISIBLE_MOVES = (3,8,13,18)
    
    def update_tickets(self, tickets_double, tickets_cab,
            tickets_bus, tickets_underground, tickets_black):
        self.tickets_double = tickets_double
        self.tickets_cab = tickets_cab
        self.tickets_bus = tickets_bus
        self.tickets_underground = tickets_underground
        self.tickets_black = tickets_black
    
class Player(PlayerGeneric):
    
    def __init__(self, start_node, name='', is_x=False):
        super(Player,self).__init__(name)
        self.start_node = start_node
        self.is_x = is_x
    
    def init_x(self, police_count):
        self.tickets_double = 2
        self.tickets_cab = 4
        self.tickets_bus = 3
        self.tickets_underground = 3
        self.tickets_black = police_count
        self.x_pub = PlayerX(self.name)
        return self.x_pub
    
    def is_visible(self):
        return len(self.moves) in self.x_pub.VISIBLE_MOVES
        
    def add_ticket(self, ticket_type):
        ticket_attr = 'tickets_%s' % ticket_type
        ticket_count = getattr(self,ticket_attr)
        setattr(self, ticket_attr, ticket_count + 1)
        
    
    def update_x(self):
        self.x_pub.update_tickets(self.tickets_double, self.tickets_cab,
            self.tickets_bus, self.tickets_underground, self.tickets_black)
        if len(self.x_pub.moves) + 1 in self.x_pub.VISIBLE_MOVES:
            self.x_pub.moves.append(self.moves[-1])
        else:
            self.x_pub.moves.append(self.moves[-1].clone_hidden())
        
    def draw(self, move, graph):
        ticket_attr = 'tickets_%s' % move.ticket
        ticket_count = getattr(self,ticket_attr)
        if ticket_count < 1:
            raise InvalidMoveError("No more %s tickets avaiable." % move.ticket)
        if not move.target in graph.neighbors(self.get_position()):
            raise InvalidMoveError()
        setattr(self, ticket_attr, ticket_count - 1)
        self.moves.append(move)
        if self.is_x:
            self.update_x()
    
    def get_position(self):
        if len(self.moves):
            return self.moves[-1].target
        return self.start_node
    
    def get_old_position(self):
        if len(self.moves) >1:
            return self.moves[-2].target
        return self.start_node
    
class InvalidMoveError(exceptions.Exception):
    pass

class EndOfGame(exceptions.Exception):
    pass


def random_select(position_list):
    r = random.randint(0,len(position_list)-1)
    # r = 0
    position = position_list[r]
    del position_list[r]
    return position, position_list
    
if __name__ == '__main__':
    import sys
    from mr_x import MrX
    from police import Police
    police_count = 5
    log_core = 40
    log_mrx = 40
    log_police = 40
    config_file = 'config.cfg'
    try:
        for arg in sys.argv[1:]:
            if arg[0:9] == '--police=':
                police_count = int(arg[9:])
            elif arg[0:10] == '--log-lvl=':
                log_core = int(arg[10:])
            elif arg[0:10] == '--log-mrx=':
                log_mrx = int(arg[10:])
            elif arg[0:10] == '--log-pol=':
                log_police = int(arg[10:])
            elif arg[0:9] == '--config=':
                config_file = arg[9:]
            else:
                raise exceptions.ValueError()
    except:
        print """
Explanation comes here
--config=FILE       use custom config file. default=config.cfg
--police=NUMBER     number of police. default=5
-h                  show this help text

Logging
--log-lvl=NUMBER    custom log level for main application. default=40
--log-mrx=NUMBER    custom log level for mr x module. default=40
--log-pol=NUMBER    custom log level for police module. default=40
"""
        exit()
            
    application = Application(Police,MrX,police_count=police_count, log_core=log_core, log_mrx=log_mrx, log_police=log_police)
    application.play()