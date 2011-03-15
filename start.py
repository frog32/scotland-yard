import exceptions
import networkx as nx
import random

VERBOSITY = 0

class Application(object):
    police_module, mr_x_module = None, None
    graph = None
    start_positions = []
    def __init__(self, police_module, mr_x_module, police_count=5):
        self.load_map()
        if VERBOSITY >= 1:
            print 'Created Map'
        self.polices = []
        position, positions = random_select(self.start_positions[:])
        self.x = Player(position, 'Mr X', True) # start position 
        self.x_pub = self.x.init_x(police_count)
        if VERBOSITY >= 1:
            print 'Created %s' % self.x
        for i in range(police_count):
            position, positions = random_select(positions)
            police = Player(positions, 'Police %s' % (i+1)) # startnode is i for testing purposes
            self.polices.append(police)
            if VERBOSITY >= 1:
                print 'Created %s' % police
        del positions
        self.mr_x_module = mr_x_module(self.graph, self.x, self.polices, Move)
        self.police_module = police_module(self.graph, self.x_pub, self.polices, Move)
        # ready to start game
        print "init completed"
        
    def play(self):
        players = [self.x] + self.polices
        for i in range(22):
            print "round %s" % i
            for player in players:
                if player.is_x:
                    module = self.mr_x_module
                else:
                    module = self.police_module
                move = module.draw(i,player)
                player.draw(move, self.graph)
                if player.is_x:
                    player.update_x(-1)
                else:
                    self.x.add_ticket(move.ticket)
                print "%s went to %s by %s" % (player, move.target, move.ticket)
    
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
    
    def clone_hidden(self):
        return Move(None ,self.ticket)

class PlayerGeneric(object):
    tickets_cab = 10
    tickets_bus = 8
    tickets_unerground = 4
    tickets_black = 0
    tickets_double = 0
    moves = []
    name = None
    
    def __repr__(self):
        return self.name

class PlayerX(PlayerGeneric):
    def __init__(self,):
        self.visible_until_move = -1
        self.name = "Mr. X"
    
    def update_tickets(self, tickets_double, tickets_cab,
            tickets_bus, tickets_unerground, tickets_black):
        self.tickets_double = tickets_double
        self.tickets_cab = tickets_cab
        self.tickets_bus = tickets_bus
        self.tickets_unerground = tickets_unerground
        self.tickets_black = tickets_black
    
    def clear_invisible_moves(self):
        self.moves = self.moves[:self.visible_until_move+1]

class Player(PlayerGeneric):
    
    def __init__(self, start_node, name='', is_x=False):
        self.start_node = start_node
        self.name = name
        self.is_x = is_x
    
    def init_x(self, police_count):
        self.tickets_double = 2
        self.tickets_cab = 4
        self.tickets_bus = 3
        self.tickets_unerground = 3
        self.tickets_black = police_count
        self.x = PlayerX()
        self.update_x(0)
    
    def add_ticket(self, ticket_type):
        ticket_attr = 'tickets_%s' % ticket_type
        ticket_count = getattr(self,ticket_attr)
        setattr(self, ticket_attr, ticket_count + 1)
        
    
    def update_x(self, visible_until_move):
        self.x.update_tickets(self.tickets_double, self.tickets_cab,
            self.tickets_bus, self.tickets_unerground, self.tickets_black)
        if visible_until_move > self.x.visible_until_move:
            self.x.clear_invisible_moves()
            for m in self.moves[len(self.x.moves):]:
                self.x.moves.append(m)
            self.x.visible_until_move = visible_until_move
        else:
            for m in self.moves[len(self.x.moves):]:
                self.x.moves.append(m.clone_hidden())
        
    def draw(self, move, graph):
        ticket_attr = 'tickets_%s' % move.ticket
        ticket_count = getattr(self,ticket_attr)
        if ticket_count < 1:
            raise InvalidMove("No more %s tickets avaiable." % move.ticket)
        if not move.target in graph.neighbors(self.get_position()):
            raise InvalidMove()
        setattr(self, ticket_attr, ticket_count - 1)
        self.moves.append(move)
    
    def get_position(self):
        if len(self.moves):
            return self.moves[-1].target
        return self.start_node
    
class InvalidMove(exceptions.Exception):
    pass    

def random_select(position_list):
    r = random.randint(0,len(position_list)-1)
    position = position_list[r]
    del position_list[r]
    return position, position_list
    
if __name__ == '__main__':
    import sys
    from mr_x import MrX
    from police import Police
    police_count = 5
    try:
        for arg in sys.argv[1:]:
            if arg[0:9] == '--police=':
                rounds = int(arg[9:])
            elif arg == '-v':
                VERBOSITY += 1
            elif arg[-4:] == '.csv':
                NAMES, DISTANCES = read_file(arg)
            else:
                raise exceptions.ValueError()
    except:
        print """
Explanation comes here
--police=NUMBER number of police
-v              Be verbose.
"""
        exit()
            
    application = Application(Police,MrX,police_count=police_count)
    application.play()