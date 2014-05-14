#! /bin/env python

#CHALLENGE DESCRIPTION

#  There is a monkey which can walk around on a planar grid. The monkey can move one space at a time left, right, up or down. 
#  That is, from (x, y) the monkey can go to (x+1, y), (x-1, y), (x, y+1), and (x, y-1). Points where the sum of the digits 
#  of the absolute value of the x coordinate plus the sum of the digits of the absolute value of the y coordinate are lesser 
#  than or equal to 19 are accessible to the monkey. For example, the point (59, 79) is inaccessible because 5 + 9 + 7 + 9 = 30, 
#  which is greater than 19. Another example: the point (-5, -7) is accessible because abs(-5) + abs(-7) = 5 + 7 = 12, which is less than 19. 
#  How many points can the monkey access if it starts at (0, 0), including (0, 0) itself?
#

import itertools
from pdb import set_trace
import sys
import ROOT
sys.setrecursionlimit((199*2)**2)
from functools import update_wrapper

def decorator(d):
    "Make function d a decorator that wraps function fn"
    return lambda fn: update_wrapper(d(fn),fn)

decorator = decorator(decorator)

@decorator
def memo(fn):
    "Decorato to memoize (cache) results of a function"
    cache = {}
    def _f(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        try: #check if we have it in cache
            return cache[key]
        except KeyError: #No, we don't
            cache[key] = result = fn(*args, **kwargs)
            return result
        except TypeError: #Actually, the args cannot even be a key of dict (like lists)
                          #print "this cannot be cached: %s" % type(args)
            return fn(*args, **kwargs)
    return _f

@memo
def sum_digits(number):
    mod = number % 10
    div = number / 10
    if div == 0:
        return mod
    else:
        return mod + sum_digits(div)

class Walker(object):
    def __init__(self):
        self.visited_tiles = set() # might be improved with a k-d tree
        self.boundary = 19
        self.graph = ROOT.TGraph()
        self.canvas = ROOT.TCanvas()
        self.graph.Draw('AP')
        self.graph.SetMarkerStyle(20)
        self.graph.SetMarkerSize(0.5)
        self.numpoints = 0

    def look_around(self, point):
        'checks wich of the neighboring tiles are accessible and not yet covered'
        for ds in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = tuple(i+j for i, j in zip(point, ds))

            sumx = sum_digits(abs(x))
            sumy = sum_digits(abs(y))

            if sumx + sumy <= self.boundary \
               and (x, y) not in self.visited_tiles and \
               x >= 0 and y >= 0:
                yield (x, y)

    def walk(self, starting_point):
        self.visited_tiles.add(starting_point)
        #self.graph.SetPoint(self.numpoints, *starting_point)
        self.numpoints += 1
        if self.numpoints % 1000 == 0:
            self.graph.Draw('AP')
            self.canvas.Update()
        for new_point in self.look_around(starting_point):
            self.walk(new_point)
        return

    def stack_walk(self, starting_point):
        '''non-recursive version of walk'''
        self.visited_tiles = set() #empty set, free some memory
        visited_tiles = set() #local version
        boundary = self.boundary #minimize self calls
        stack = [starting_point]
        visited_tiles.add(starting_point)
        iteration = 0
        while stack: #test if empty
            iteration += 1
            point = stack.pop()
            self.graph.SetPoint(iteration, *point)
            if iteration % 1000 == 0:
                self.graph.Draw('AP')
                self.canvas.Update()
            x, y  = point
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                newx = x+dx
                newy = y+dy
                sumx = sum_digits(abs(newx))
                sumy = sum_digits(abs(newy))
                #check boundary condition
                if sumx + sumy > boundary:
                    continue
                #check if already covered
                if (newx, newy) in visited_tiles:
                    continue
                visited_tiles.add((newx, newy))
                stack.append((newx, newy))
        return visited_tiles


chuck_norris = Walker()
chuck_norris.walk((0,0))
num_tiles    = len(chuck_norris.visited_tiles)
print "number of tiles visited: %i" % num_tiles
tiles_on_x_axis = len(
    filter(
        lambda x: x[1] == 0, chuck_norris.visited_tiles
        )
    )
tiles_on_y_axis = len(
    filter(
        lambda x: x[0] == 0, chuck_norris.visited_tiles
        )
    )
assert(tiles_on_x_axis == tiles_on_y_axis)
#use symmetry to guess the total number of accessible tiles
accessible_tiles = 4*(num_tiles - 2*tiles_on_y_axis) #Symmetry in X and Y axis, do not count tiles on the axes
accessible_tiles += (2*tiles_on_y_axis + 2*tiles_on_x_axis) #add tiles on the axes
accessible_tiles -= 3 #remove the origin, that has been double-counted three times (is present in both the axes)
print "total number of accessible tiles: %i" % accessible_tiles
visited_tiles = chuck_norris.stack_walk((0,0))
print "as from stack walk: %i" % len(visited_tiles)

#lines = open('tiles.txt').readlines()
#lines = [i.strip() for i in lines]
#lines = [tuple(i.split()) for i in lines]
#tiles = [(int(x),int(y)) for x,y in lines]
#del lines
#cpp_tiles = set(tiles)
#print len(cpp_tiles) == len(tiles)
#del tiles
#print cpp_tiles.issubset(visited_tiles)
#difference = visited_tiles.difference(cpp_tiles)
#del cpp_tiles
#del visited_tiles 
#is_ok = [ sum_digits(abs(x)) + sum_digits(abs(y)) for x, y in diff]
