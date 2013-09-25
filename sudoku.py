import sys

def main():
  # initialize game board to 0s
  # TODO: initialize to something like undefined to have the possiblity
  # to get user to define the board
  board = [[0 for x in xrange(9)] for x in xrange(9)]

  # a board of possible numbers to fill in the board
  possibilities = [[[-1 for x in xrange(9)] for x in xrange(9)] for x in xrange(9)]
  # 0 means number is put down
  # 1 means number can be put down
  # > 1 means more filtering required
  numpos = [[9 for x in xrange(9)] for x in xrange(9)]

  # fill game board with pre-made sudoku games
  # TODO: let user input
  i = 0;
  with open('sudoku_input.txt', 'r') as f:
    for line in f:
      board[i] = line.strip().split()
      i += 1

  initializePossiblityGrid(board, possibilities, numpos);

  print_board(board)
  print ''

  done = True
  while (done):
    for x in range(0, 9):
      for y in range(0, 9):
        if (numpos[x][y] == 1):
          board[x][y] = possibilities[x][y][0]
    initializePossiblityGrid(board, possibilities, numpos);
    done = checkIfDone(board)
        
  print_board(board)  
  # print_possibility_grid(possibilities)
  # print numpos

def checkIfDone(board):
  for x in range(0, 9):
      if ('0' in board[x]): 
        return False;
  return True

def getTopLeftGridPos(x, y):
  returnX = 0
  returnY = 0
  if (y % 3 == 0): #left
    returnY = y
  elif (y % 3 == 1): # mid
    returnY = y-1  
  else: # right
    returnY = y-2

  if (x % 3 == 0): # top right
    returnX = x
  elif (x % 3 == 1): # mid
    returnX = x-1
  else: # bottom right
    returnX = x-2

  return (returnX, returnY)

def initializePossiblityGrid(board, pos, npos):
  # iterate through the board and define all the possible numbers
  for i in range(0, 9):
    for j in range(0, 9):
      # cell is filled
      if (board[i][j] != '0'):
        pos[i][j] = []
        npos[i][j] = 0
      # cell is unfilled
      else:
        tmp = ['1','2','3','4','5','6','7','8','9']
        # check column
        for y in range(0, 9):
          if (board[i][y] in tmp):
            tmp.remove(board[i][y])
        # check grid
        pair = getTopLeftGridPos(i, j)
        pairX = pair[0]
        pairY = pair[1]
        for x in range(0, 3):
          for y in range(0, 3):
            if (board[pairX+x][pairY+y] in tmp):
              tmp.remove(board[pairX+x][pairY+y])
        # check line
        for x in range(0, 9):
          if (board[x][j] in tmp):
            tmp.remove(board[x][j])
        pos[i][j] = tmp
        npos[i][j] = len(tmp)      

def print_board(board):
  for x in range(0, 9):
    for y in range(0, 9):
      sys.stdout.write(board[x][y])
      sys.stdout.write(' ')
      sys.stdout.flush()
    print ''

def print_possibility_grid(grid):
  for x in range(0, 9):
    for y in range(0, 9):
      print grid[x][y]    
      print ''

main()

