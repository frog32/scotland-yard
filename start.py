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
            police = Player(position, 'Police %s' % (i+1)) # startnode is i for testing purposes
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
                if not player.is_x:
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
            print self
            self.update_x()
    
    def get_position(self):
        if len(self.moves):
            print self.moves
            print "%s zug gemacht" % self
            return self.moves[-1].target
        print "erster zug"
        return self.start_node
    
class InvalidMoveError(exceptions.Exception):
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
                police_count = int(arg[9:])
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