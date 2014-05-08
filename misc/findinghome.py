#"Bob has become lost in his neighborhood. He needs to get from his current position back to his home. Bob's neighborhood is a 2 dimensional grid, that starts at (0, 0) and (width - 1, height - 1). There are empty spaces upon which bob can walk with no difficulty, and houses, which Bob cannot pass through. Bob may only move horizontally or vertically by one square at a time. 
#
#Bob's initial position will be represented by a 'B' and the house location will be represented by an 'H'. Empty squares on the grid are represented by '.' and houses are represented by 'X'. Find the minimum number of steps it takes Bob to get back home, but if it is not possible for Bob to return home, return -1. 
#
#An example of a neighborhood of width 7 and height 5:
#
#...X..B
#.X.X.XX
#.H.....
#...X...
#.....X."

example = '''...X..B
.X.X.XX
.H.....
...X...
.....X.'''

import itertools
from pdb import set_trace
from Queue import PriorityQueue

def build_info(string):
    town_map = string.split('\n') #[Y][X]
    town_map = zip(*town_map) #[X][Y]
    width    = len(town_map)
    height   = len(town_map[0])
    bob = None
    home = None
    for x1, y1 in itertools.product(xrange(width), xrange(height)):
        if town_map[x1][y1] == 'B':
            bob = (x1, y1)
        elif town_map[x1][y1] == 'H':
            home = (x1, y1)
    return {
        'town_map' : town_map,
        'width'    : width ,
        'height'   : height,
        'bob'      : bob   ,
        'home'     : home  ,
        }

class Point2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def adjacent_distance(char1, char2):
    return -2 if char1 == 'X' or char2 == 'X' else 1

#Stack
def Stack(
        town_map = [],
        width    = 0 ,
        height   = 0,
        bob      = (0,0),
        home     = (0,0)): 
    stack = []
    visited = [[ False for _ in xrange(height)] for _ in xrange(width)]
    min_step = width*height
    stack.append((0, bob))
    while len(stack) > 0:
        steps_done, location = stack.pop()
        x, y = location
        visited[x][y] = True
        #move by dxy
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            new_x = x+dx
            new_y = y+dy
            #Check that new_x,y within bounds
            if new_x < 0 or new_x >= width:
                continue
            if new_y < 0 or new_y >= height:
                continue

            #check if I am home
            if town_map[new_x][new_y] == 'H':
                min_step = min((min_step, steps_done+1))
                continue
            #or on a house
            elif town_map[new_x][new_y] == 'X':
                continue
            #or I've already been here
            elif visited[new_x][new_y]:
                continue

            #visited[new_x][new_y] = True
            stack.append((steps_done+1, (new_x, new_y)))
    return min_step if min_step < width*height else -2


#Dijkstra 
def Dijkstra(
        town_map = [],
        width    = 0 ,
        height   = 0,
        bob      = (0,0),
        home     = (0,0)): 
    queue = PriorityQueue()
    visited = [[ False for _ in xrange(height)] for _ in xrange(width)]
    #set_trace()
    visited[bob[0]][bob[1]] = True
    queue.put((0, bob))
    while not queue.empty():
        steps_done, location = queue.get()
        x, y = location
        #move by dxy
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            new_x = x+dx
            new_y = y+dy
            #Check that new_x,y within bounds
            if new_x < 0 or new_x >= width:
                continue
            if new_y < 0 or new_y >= height:
                continue

            #check if I am home
            if town_map[new_x][new_y] == 'H':
                return steps_done+1
            elif town_map[new_x][new_y] == 'X':
                continue
            elif visited[new_x][new_y]:
                continue

            visited[new_x][new_y] = True
            queue.put((steps_done+1, (new_x, new_y)))
    return -2


#Floyd_Warshall
def Floyd_Warshall(
        town_map = [],
        width    = 0 ,
        height   = 0,
        bob      = (0,0),
        home     = (0,0)): #(slowest but fastest to code)
    adjacency_map = [] #4D list (x1, y1, x2, y2) -1 not set, -2 Impassable, 
    for x1 in xrange(width):
        x1Line = []
        for y1 in xrange(height):
            y1Line = []
            for x2 in xrange(width):
                y1Line.append([-1 for _ in xrange(height)])
            x1Line.append(y1Line)
        adjacency_map.append(x1Line)

    for x1, y1 in itertools.product(xrange(width), xrange(height)):
        xdeltas = []
        if x1 == 0:
            xdeltas = [1]
        elif x1 == (width-1):
            xdeltas = [-1]
        else:
            xdeltas = [-1, 1]

        ydeltas = []
        if y1 == 0:
            ydeltas = [1]
        elif y1 == (height-1):
            ydeltas = [-1]
        else:
            ydeltas = [-1, 1]

        tile_char = town_map[x1][y1]
        for xd in xdeltas:
            x2 = x1 + xd
            adjacency_map[x1][y1][x2][y1] = \
                adjacent_distance(
                    tile_char, 
                    town_map[x2][y1]
                )

        for yd in ydeltas:
            y2 = y1 + yd
            adjacency_map[x1][y1][x1][y2] = \
                adjacent_distance(
                    tile_char, 
                    town_map[x1][y2]
                )

    for x1, y1 in itertools.product(xrange(width), xrange(height)):
        tile_char = town_map[x1][y1]
        if tile_char == 'X':
            for x2, y2 in itertools.product(xrange(width), xrange(height)):
                adjacency_map[x1][y1][x2][y2] = -2
                adjacency_map[x2][y2][x1][y1] = -2

    #set_trace()
    counts = 9
    limit  = 4
    num_it = 0
    while counts > 0 and num_it < limit:
        num_it += 1
        for x1, y1 in itertools.product(xrange(width), xrange(height)):
            for x2, y2 in itertools.product(xrange(width), xrange(height)):
                for x3, y3 in itertools.product(xrange(width), xrange(height)):
                    d_12 = adjacency_map[x1][y1][x2][y2]
                    d_23 = adjacency_map[x2][y2][x3][y3]
                    d_13 = adjacency_map[x1][y1][x3][y3]
                    d_132 = -1
                    if d_23 > 0 and d_13 > 0:
                        d_132 = d_23 + d_13
                    elif d_23 == -2 or d_13 == -2:
                        d_132 = -2
                    if d_12 < 0:
                        adjacency_map[x1][y1][x2][y2] = d_132
                    else:
                        if d_132 > 0:
                            adjacency_map[x1][y1][x2][y2] = min([d_132, d_12])
                    #if adjacency_map[x1][y1][x2][y2] == -1 and num_it == 2:
                    #    print d_12, d_23, d_13, d_132
                    #    set_trace()

        counts = 0
        for x1, x2, y1, y2 in itertools.product(xrange(width), xrange(width), xrange(height), xrange(height)):
            if adjacency_map[x1][y1][x2][y2] == -1:
                counts += 1

    assert(adjacency_map[bob[0]][bob[1]][home[0]][home[1]] == adjacency_map[home[0]][home[1]][bob[0]][bob[1]])
    return adjacency_map[bob[0]][bob[1]][home[0]][home[1]]
    
info = build_info(example)
print "Distance Floyd-Warshall 1 %i" % Floyd_Warshall(**info)
print "Distance Dijkstra       1 %i" % Dijkstra(**info)
#print "Distance Stack          1 %i" % Stack(**info)

example = '''...XB
...XX
H....'''
info = build_info(example)
print "Distance Floyd-Warshall 2 %i" % Floyd_Warshall(**info)
print "Distance Dijkstra       2 %i" % Dijkstra(**info)
#print "Distance Stack          2 %i" % Stack(**info)

example = '''......B
XXXX.X.
..HX.X.
.XXX.X.
.......'''
info = build_info(example)
print "Distance Floyd-Warshall 3 %i" % Floyd_Warshall(**info)
print "Distance Dijkstra       3 %i" % Dijkstra(**info)
#print "Distance Stack          3 %i" % Stack(**info)
