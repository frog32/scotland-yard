from sets import Set
import networkx as nx
from start import Move

class CopMove(Move):
    def __init__(self, cop, target, ticket):
        super(CopMove,self).__init__(target, ticket)
        self.cop = cop

    def __repr__(self):
        return 'cop %s to target %s with %s' % (self.cop, self.target, self.ticket)

def get_mr_x_position(graph, mr_x, move_cls):
    moves = mr_x.moves[:]
    moves.reverse()
    tickets = []
    visible_position = None
    for m in moves:
        if not m.target is None:
            visible_position = m.target
            break
        else:
            tickets.append(m.ticket)
    position = []
    tickets.reverse()
    if not visible_position is None:
        position = getPlaces(graph, visible_position, tickets)

    return position

def getPlaces(graph, position, tickets):
    if len(tickets) == 0:
        return [position]
    ticket = tickets[0]
    choices = graph.neighbors(position)
    places = []
    for c in choices:
        transport = graph[position][c]
        for t in transport:
            if transport[t]['ticket']==ticket:
                if len(tickets)==1:
                    places.append(c)
                else:
                    tix = tickets[:]
                    tix.pop(0)
                    places.extend(getPlaces(graph,c,tix))
    return list(set(places))

def getMrxRoutes(graph, policemen, mr_x, move_cls):
    posishs = get_mr_x_position(graph, mr_x, move_cls)
    return getRoutes(graph, policemen, posishs)

def getCopPosish(cop):
    if len(cop.moves) == 0:
        return cop.start_node
    else:
        return cop.moves[-1].target

def getRoutes(graph, policemen, posishs):
    shortest_paths = []
    for cop in policemen:
        options = Move_Options(cop)
        co_posish = getCopPosish(cop)
        for posish in posishs:
            if not co_posish == posish:
                options.paths.append(nx.shortest_path(graph, co_posish, posish))
        shortest_paths.append(options)
    return shortest_paths

class Move_Options(object):
    paths = []
    def __init__(self, cop):
        self.cop = cop
        self.paths = []

    def __repr__(self):
        return "Cop %s can go %s" % (self.cop, self.paths)

    def shortest(self):
        shortest_paths = []
        length = 200
        for path in self.paths:
            if length > len(path) and not len(path) == 1:
                shortest_paths = [path]
                length = len(path)
            elif length == len(path):
                shortest_paths.append(path)
        return shortest_paths

# return the type of ticket the cop should use
def evaluate_ticket(graph, cop, target):
    last_target = getCopPosish(cop)
    got_bus = False
    got_taxi = False
    got_ubahn = False
    for tries in [0,1,2]:
        try:
            ticket = graph[last_target][target][tries]['ticket']
            if ticket == 'bus':
                got_bus = True
            elif ticket == 'cab':
                got_taxi = True
            elif ticket == 'underground':
                got_ubahn = True
        except:
            pass
    if got_taxi and not got_ubahn and not got_bus:
        return 'cab'
    elif got_bus and not got_taxi and not got_ubahn:
        return 'bus'
    elif got_ubahn and not got_taxi and not got_bus:
        return 'underground'
    else: # got_bus and got_taxi
        if cop.tickets_cab > cop.tickets_bus:
            return 'cab'
        else:
            return 'bus'


goodplaces = []

# returns a list of goodplaces
def get_goodplaces(graph):
    if len(goodplaces)==0:
        for node in nx.nodes(graph):
            got_bus = False
            got_taxi = False
            got_ubahn = False
            for edge in nx.edges(graph,node):
                for tries in [0,1,2]:
                    try:
                        ticket = graph[edge[0]][edge[1]][tries]['ticket']
                        if ticket == 'bus':
                            got_bus = True
                        elif ticket == 'cab':
                            got_taxi = True
                        elif ticket == 'underground':
                            got_ubahn = True
                    except:
                        pass
            if got_bus & got_taxi & got_ubahn:
                goodplaces.append(node)
    return goodplaces

# returns a list of Move objects
def go_to_goodplace(whenshow, graph, polices, mr_x, move_cls):
    routes_to_goodplace = getRoutes(graph, polices, get_goodplaces(graph))
    steps = 5 - whenshow
    moves = []
    copi = 0
    for route in routes_to_goodplace:
        success = False
        for path in route.paths:
            if polices[copi].tickets_underground <= 1:
                break
            if len(path) == steps+1 and not success:
                moves.append(CopMove(polices[copi], path[1], evaluate_ticket(graph, polices[copi], path[1])))
                success = True
        if not success:
            cop = polices[copi]
            if not cop.tickets_bus < 2 and not cop.tickets_cab < 2 and not cop.tickets_underground < 1:
                moves.append(try_to_catch_single(graph, cop, mr_x, move_cls, find_nogoes(moves)))
            else:
                moves.append(try_to_escape(graph,cop,mr_x, move_cls, find_nogoes(moves)))
        copi = copi + 1
    return moves

def find_nogoes(moves):
    no_goes = []
    for move in moves:
        no_goes.append(move.target)
    return no_goes

def try_to_escape(graph, cop, mr_x, move_cls, no_goes):
    posish = getCopPosish(cop)
    neighbors = graph.neighbors(posish)
    success = False
    for neighbor in neighbors:
        if cop.tickets_bus <= cop.tickets_cab:
            if evaluate_ticket(graph, cop, neighbor) == 'cab':
                target = neighbor
                success = True
        elif cop.tickets_bus > cop.tickets_cab:
            if evaluate_ticket(graph, cop, neighbor) == 'bus':
                target = neighbor
                success = True
        elif cop.tickets_bus == 0 and cop.tickets_cab == 0:
            if evaluate_ticket(graph, cop, neighbor) == 'underground':
                target = neighbor
                success = True
    if not success:
        print('screw you guys, im going home')
        if not cop.tickets_underground == 0:
            return CopMove(cop, neighbors[0], 'underground')
        elif not cop.tickets_cab == 0:
            return CopMove(cop, neighbors[0], 'cab')
        elif not cop.tickets_bus == 0:
            return CopMove(cop, neighbors[0], 'bus')
    return CopMove(cop, target, evaluate_ticket(graph, cop, neighbors))

# returns a list of Move objects for each cop
def try_to_catch(graph, polices, mr_x, move_cls):
    moves = []
    for cop in polices:
        no_goes = find_nogoes(moves)
        if not cop.tickets_bus < 2 and not cop.tickets_cab < 2 and not cop.tickets_underground < 1:
            moves.append(try_to_catch_single(graph, cop, mr_x, move_cls, no_goes))
        else:
            moves.append(try_to_escape(graph,cop,mr_x, move_cls, no_goes))
    return moves

# returns the number of the most popular target step
def get_popular_step(options, no_goes):
    steps = []
    for option in options.paths:
        success = False
        if not option[1] in no_goes:
            steps.append(option[1])
            success = True
        if not success:
            steps.append(options.paths[0][1])
    steps.sort()
    final_target = None
    final_count = 0
    temp_target = None
    temp_count = 0
    for step in steps:
        if temp_target==None:
            temp_target = step
            temp_count = 1
        elif temp_target==step:
            temp_count = temp_count + 1
        else:
            if final_count < temp_count:
                final_target = temp_target
                final_count = temp_count
            temp_count = 1
            temp_target = step
    if final_target == None:
        final_target = temp_target
    return final_target

def make_random_move(graph, cop, no_goes):
    posish = getCopPosish(cop)
    neighbors = graph.neighbors(posish)
    success = False
    for neighbor in neighbors:
        if not neighbor in no_goes:
            target = neighbor
            success = True
    if not success:
        target = neighbors[0]
    return CopMove(cop, target, evaluate_ticket(graph, cop, target))

# returns a Move object for a single cop
def try_to_catch_single(graph, cop, mr_x, move_cls, no_goes):
    routes = getMrxRoutes(graph, [cop], mr_x, move_cls)
    if len(routes[0].paths) == 0:
        return make_random_move(graph, cop, no_goes)
    options = routes[0]
    shortest_options = options.shortest()
    move = None
    for opt in shortest_options:
        if not opt[1] in no_goes:
            move = CopMove(cop, opt[1], evaluate_ticket(graph, cop, opt[1]))
            break
    if move == None:
        target = get_popular_step(options, no_goes)
        move = CopMove(cop, target, evaluate_ticket(graph, cop, target))
    if move == None:
        move = make_random_move(graph, cop, no_goes)
    return move
