import itertools
from collections import Counter
import copy

class Cell(object):
    def __init__(self, val=-1, opt=''):
        self.value   = val
        self.options = [val] if val != -1 else range(1,10)
        self.locked  = (val != -1)
        
    def pop(self, val):
        if val in self.options and not self.locked:
            index = self.options.index(val)
            self.options.pop(index)
            if len(self.options) == 1:
                self.locked = True
                self.value  = self.options[0]
            return True
        else:
            return False

    def __repr__(self):
        if self.locked:
            return self.value.__repr__()
        else:
            return ' '

class SudokuError(ValueError):
    def __init__(self, *args, **kwargs):
        super(SudokuError, self).__init__(*args, **kwargs)

class Board(object):
    def __init__(self, definition):
        '''
        board = open('bard_check.txt').read()
        b = Board( board )
        print b
        '''
        self.board = []
        for line in [i for i in definition.split('\n') if i and i[0] != '-']:
            parsed_line = []
            for i in line.split('|'):
                if not i:
                    continue
                txt_cell = i.strip()
                if txt_cell:
                    parsed_line.append( Cell( int(txt_cell) ) )
                else:
                    parsed_line.append( Cell() )
            self.board.append(parsed_line)

    def __repr__(self):
        line_lenght = 0
        ret = ''
        for line in self.board:
            ret += '| '+' | '.join('%s' % i for i in line)+' |\n'
            if not line_lenght:
                line_lenght = len(ret)-1
            ret += '-'*line_lenght+'\n'
        return '-'*line_lenght+'\n'+ret

    @staticmethod
    def check( cellist ):
        'check that two cells dont have the same locked value'
        values = [ i.value for i in cellist if i.locked ]
        if values:
            return (max(Counter(values).values()) == 1)
        else:
            return True

    @staticmethod
    def reduce( cellist ):
        'removes all the occurrences of locked cells'
        values   = [ i.value for i in cellist if i.locked ]
        modified = False
        for val in values:
            modified = any([cell.pop(val) for cell in cellist])# + [modified])
        if modified:
            return True, Board.reduce( cellist )[1]
        else:
            return False, cellist

    @staticmethod
    def reduce_all( cellmap ):
        rets = [ Board.reduce( i ) for i in cellmap ]
        return reduce(
            lambda x, y: (x[0] or y[0], x[1] + [y[1]]),
            rets, 
            (False, []) )

    @property
    def squares(self):
        ret = []
        for square_id in range(9):
            minx = (square_id % 3)*3
            maxx = minx+3
            miny = (square_id / 3)*3
            maxy = miny+3
            square  = []
            for i in range(miny, maxy):
                square.extend(self.board[i][minx:maxx])
            ret.append(square)
        return ret

    @squares.setter
    def squares(self, squares):
        for index, cellist in enumerate( squares ):
            minx = (index % 3)*3
            maxx = minx+3
            miny = (index / 3)*3
            maxy = miny+3
            counter = 0
            for i in range(miny, maxy):
                for j in range(minx, maxx):
                    self.board[i][j] = cellist[counter]
                    counter += 1
        

    def set_square(self, index, cellist):
        minx = (index % 3)*3
        maxx = minx+3
        miny = (index / 3)*3
        maxy = miny+3
        counter = 0
        for i in range(miny, maxy):
            for j in range(minx, maxx):
                self.board[i][j] = cellist[counter]
                counter += 1

    def column(self, index):
        return [i[index] for i in self.board]

    def set_column(self, index, column):
        for i in range( len( self.board ) ):
            self.board[i][index] = column[i]

    @property 
    def columns(self):
        return [[i[index] for i in self.board] for index in range(9)]

    @columns.setter 
    def columns(self, cols):
        for i, col in enumerate(cols):
            for j, val in enumerate( col ):
                self.board[j][i] = cols[i][j]

    def is_ok(self):
        ok = all( Board.check( line ) for line in self.board )
        ok = ok and all( Board.check( i ) for i in self.columns )
        ok = ok and all( Board.check( i ) for i in self.squares )
        return ok

    def solve(self, do_fork = True):
        modified = True
        counter = 0
        while modified:
            #print "iteration %i" % counter
            #counter += 1
            #reduce lines
            l, self.board = Board.reduce_all( self.board )
            #reduce columns
            c, self.columns = Board.reduce_all( self.columns )
            #reduce squares
            s, self.squares = Board.reduce_all( self.squares )
            modified = any([l, c, s])
            #check if all rules apply
            if not self.is_ok():
                return False, self.board
        
        if not self.is_done():
            if do_fork:
                options = self.fork()
                solved, board = False, None
                for opt in options:
                    solved, board = opt.solve()
                    if solved:
                        break
                self.board = board
                return solved, board
            else:
                return True, self.board
        else:
            return True, self.board
        #print self.__repr__()

    def is_done(self):
        return all( self.board[i][j].locked for i, j in itertools.product(range(9), range(9)) )

    def fork(self):
        min_options = 10
        coords = (-1, -1)
        for i in range(9):
            for j in range(9):
                if not self.board[i][j].locked and \
                   len( self.board[i][j].options ) < min_options:
                    coords = (i, j)
                    min_options = len( self.board[i][j].options )
        
        ret = []
        for opt in self.board[coords[0]][coords[1]].options:
            ret.append( copy.deepcopy(self) )
            ret[-1].board[coords[0]][coords[1]] = Cell( opt )
        return ret
        
        
#-------------------------------------
#| 5 | 7 | 6 | 3 | 2 | 4 | 9 | 8 | 1 |
#-------------------------------------
#| 2 | 3 | 1 | 8 | 9 | 7 | 5 | 6 | 4 |
#-------------------------------------
#| 8 | 4 | 9 | 5 | 6 | 1 | 7 | 2 | 3 |
#-------------------------------------
#| 6 | 1 | 4 | 2 | 8 | 5 | 3 | 9 | 7 |
#-------------------------------------
#| 7 | 5 | 2 | 9 | 4 | 3 | 6 | 1 | 8 |
#-------------------------------------
#| 3 | 9 | 8 | 1 | 7 | 6 | 2 | 4 | 5 |
#-------------------------------------
#| 4 | 2 | 7 | 6 | 3 | 8 | 1 | 5 | 9 |
#-------------------------------------
#| 9 | 8 | 5 | 7 | 1 | 2 | 4 | 3 | 6 |
#-------------------------------------
#| 1 | 6 | 3 | 4 | 5 | 9 | 8 | 7 | 2 |
#-------------------------------------
