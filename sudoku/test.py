from sudoku import *

boards = open('bard_check.txt').read().split('.')
b = Board( boards[0] )
print ( b.__repr__() == boards[0])

try:
    raise SudokuError('ciccio')
except SudokuError:
    print 'sudoku error raised'

print 'columns:'
for i, col in enumerate( b.columns ):
    print i, col

print 'square:'
for i, sq in enumerate( b.squares ):
    print i, sq

b.solve()

b = Board( boards[1] )
b.solve(False)
print (b.column(0).__repr__() == range(1,10).__repr__())

b = Board( boards[2] )
b.solve(False)
print (b.board[0].__repr__() == range(1,10).__repr__())

b = Board( boards[3] )
b.solve(False)
print (b.squares[0].__repr__() == range(1,10).__repr__())

b = Board( boards[-1] )
ret = b.solve()
