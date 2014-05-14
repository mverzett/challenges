#Problem Statement
#In this problem, some test cases have more than one correct output. We are using a special checker to verify that the output of your program is correct. 
#This problem is about chessboards with rooks. A rook is a chess piece that moves arbitrarily far, either horizontally or vertically. Both rows and columns of chessboards in our problem are numbered starting from 0. 
#
#An n times n chessboard is called peaceful if it contains exactly n rooks and no two rooks attack each other. In other words, there cannot be two rooks in the same row or in the same column of the chessboard. A peaceful chessboard can be described by a int[] Y with n elements: for each row r, the rook in row r is in column Y[r]. 
#
#You are given two int[]s Y1 and Y2 with n elements each. Each of them represents one peaceful chessboard. 
#
#You want to change the first chessboard into the second one. There is only one type of moves you are allowed to make: On the first chessboard, you can choose two rooks in positions (r1,c1) and (r2,c2) such that r1 < r2 and c1 > c2, and move them to (r1,c2) and (r2,c1). Note that the new chessboard is peaceful again. 
#
#If changing the first chessboard into the second one is impossible, return a int[] with only one element, and that element should be -1. 
#
#Otherwise, find any valid sequence of moves that changes the first board into the second board. Each move is uniquely defined by two integers: the rows with the rooks you want to move. If we write down the two rows for each move, we get a sequence of integers that encodes the solution. If that sequence has at most 2500 integers (i.e., encodes at most 1250 moves), return a int[] with the entire sequence. Otherwise, return a int[] with just the first 2500 integers of your sequence.
# 
#Definition
#    	
#Class:	MovingRooksDiv1
#Method:	move
#Parameters:	int[], int[]
#Returns:	int[]
#Method signature:	int[] move(int[] Y1, int[] Y2)
#(be sure your method is public)
#    
# 
#Notes
#-	You are not required to find the solution that uses the smallest possible number of moves.
#-	If your return value has 2500 integers, it will be accepted if and only if it is a valid solution or a proper prefix of some valid solution.
#-	If your return value has fewer than 2500 integers, it will be accepted if and only if it's a valid solution (not a proper prefix).
# 
#Constraints
#-	Y1 will contain between 1 and 2500 elements, inclusive.
#-	Y2 will contain the same number of elements as Y1.
#-	Each element of Y1 will be between 0 and n-1, inclusive, where n is the number of elements of Y1.
#-	Each element of Y2 will be between 0 and n-1, inclusive, where n is the number of elements of Y2.
#-	All elements of Y1 will be distinct.
#-	All elements of Y2 will be distinct.

from Queue import PriorityQueue
import itertools
from pdb import set_trace
#import copy

def can_morph(test, target):
    return all(min(test[i:]) <= target[i] <= max(test[:i+1]) for i in xrange(len(test)))

def ranking(test, target):
    return -1*sum(1 for i, j in zip(test, target) if i == j)

def swap(l1, r1, r2):
    isAllowed = r1 < r2 and l1[r1] > l1[r2]
    if not isAllowed:
        return None
    ret = l1[:]
    tmp = l1[r1]
    ret[r1] = ret[r2]
    ret[r2] = tmp
    return ret

t1 = [1,0]
t2 = [0,1]
assert(can_morph(t1, t2) == True)
assert(ranking(t1, t2)   == 0)

t1 = [3,1,2,0]
t2 = [3,2,1,0]
t3 = [0,1,2,3]

print 'testing can_morph and ranking'
assert(can_morph(t1, t2) == True)
assert(ranking(t1, t2)   == -2)

assert(can_morph(t1, t3) == True)
assert(ranking(t1, t2)   == -2)

assert(can_morph(t2, t3) == True)
assert(ranking(t2, t3)   == 0)

assert(can_morph(t2, t1) == True)
assert(can_morph(t3, t2) == False)

def move(y1, y2):
    stack = PriorityQueue()
    #visited = set()
    chess_size = len(y1)
    stack.put((ranking(y1, y2), (y1, [])))
    while not stack.empty():
        #pop first element
        #set_trace()
        rank, element = stack.get()
        pos_list, swaps  = element
        #are we there yet?
        if rank == -1*chess_size:
            return swaps
        #loop over possible combinations
        for r1, r2 in itertools.combinations(range(chess_size), 2):
            #check if swap is allowed
            #isAllowed = r1 < r2 and pos_list[r1] > pos_list[r2]            
            #if not isAllowed:
            #    continue
            #clone pos_list
            new_candidate = swap(pos_list, r1, r2)
            if not new_candidate:
                continue
            #check if morphing is allowed
            if not can_morph(new_candidate, y2):
                continue            
            #compute ranking
            new_rank = ranking(new_candidate, y2)
            #put element
            stack.put((new_rank, (new_candidate, swaps+[r1,r2])))
    return [-1]


#test cases
print 'testing case 1'
ret = move([0],[0])
assert(ret == [])

print 'testing case 2'
t1 = [1,0]
t2 = [0,1]
assert(move(t1, t2) == [0, 1 ])

print 'testing case 3'
t1 = [1,2,0]
t2 = [2,0,1]
assert(move(t1, t2) == [-1 ])

print 'testing case 4'
t1 = [2,1,0,3,5,4]
t2 = [0,1,2,3,4,5]
print move(t1, t2)
#set_trace()
#MINE WORKS TOO! BUT IS NOT IN THE TEST CASE.... and mine is shorter...
#assert(move(t1, t2) == [0, 1, 0, 2, 1, 2, 4, 5 ])

print 'testing case 5'
t1 = [10,9,8,7,6,5,4,3,2,1,0]
t2 = [0,1,2,3,4,5,6,7,8,9,10]
print move(t1, t2)
#MINE WORKS TOO! BUT IS NOT IN THE TEST CASE.... and mine is WAY shorter...
#assert(move(t1, t2) == [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8, 1, 9, 1, 10, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7, 2, 8, 2, 9, 2, 10, 3, 4, 3, 5, 3, 6, 3, 7, 3, 8, 3, 9, 3, 10, 4, 5, 4, 6, 4, 7, 4, 8, 4, 9, 4, 10, 5, 6, 5, 7, 5, 8, 5, 9, 5, 10, 6, 7, 6, 8, 6, 9, 6, 10, 7, 8, 7, 9, 7, 10, 8, 9, 8, 10, 9, 10 ])
