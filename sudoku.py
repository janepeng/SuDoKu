import sys

def solve_sudoku(sudoku_input):
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
    i = 0
    with open('sudoku_input.txt', 'r') as f:
        for line in f:
            board[i] = line.strip().split()
            i += 1
    
    i = 0
    if sudoku_input != "":
        tmp = []
        for c in sudoku_input:
            if c == ' ':
                continue
            elif c == '\n':
                board[i] = tmp
                tmp = []
                i += 1
            else:
                tmp += c

    initializePossiblityGrid(board, possibilities, numpos)

    print_board(board)
    print ''

    done = False
    initializePossiblityGrid(board, possibilities, numpos)
    while (not done):
        changed = False
        deductPossibilityGrid(board, possibilities, numpos)
        advancedDeduction(board, possibilities, numpos)
        for x in range(0, 9):
            for y in range(0, 9):
                if (numpos[x][y] == 1):
                    board[x][y] = possibilities[x][y][0]
                    numpos[x][y] = 0
                    changed = True
        done = checkIfDone(board)
        if not changed:
            break

    print_board(board)
    # print_possibility_grid(possibilities)
    # print numpos
    return board

def checkIfDone(board):
    for x in range(0, 9):
        if ('0' in board[x]):
            return False
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

def checkcounts(buf, pos, npos, i, j):
    for k in pos[i][j]:
        if buf.count(k) == 1:
            pos[i][j] = [k]
            npos[i][j] = 1

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

def deductPossibilityGrid(board, pos, npos):
    # check each row, column, grid to identify all single numbers
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == '0':
                tmp = pos[i][j]
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
                # check column
                tmp = []
                for y in range(0, 9):
                    tmp.extend(pos[i][y])
                checkcounts(tmp, pos, npos, i ,j)
                # check grid
                pair = getTopLeftGridPos(i, j)
                pairX = pair[0]
                pairY = pair[1]
                tmp = []
                for x in range(0, 3):
                    for y in range(0, 3):
                        tmp.extend(pos[pairX+x][pairY+y])
                checkcounts(tmp, pos, npos, i, j)
                # check line
                tmp = []
                for x in range(0, 9):
                    tmp.extend(pos[x][j])
                checkcounts(tmp, pos, npos, i, j)

def getColumnorRow(indices):
    col = indices[0][0]
    row = indices[0][1]
    bufcol = []
    bufrow = []
    col = True
    row = True
    for i in range(1, len(indices)):
        bufcol.append(indices[i][0])
        bufrow.append(indices[i][1])
        if indices[i][0] != col:
            col = False
        if indices[i][1] != row:
            row = False
    if col:
        return [0, col, bufrow]
    if row:
        return [1, row, bufcol]
    return [2]

def clearColumn(num, col, r1, r2, pos, npos):
    for i in range(r1, r2+1):
        if num in pos[col][i]:
            pos[col][i].remove(num)
            npos[col][i] = len(pos[col][i])

def clearRow(num, row, c1, c2, pos, npos):
    for i in range(c1, c2):
        if num in pos[i][row]:
            pos[i][row].remove(num)
            npos[i][row] = len(pos[i][row])

def advancedDeduction(board, pos, npos):
    # check grid
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            buf = []
            for x in range(0, 3):
                for y in range(0, 3):
                    buf.extend(pos[i+x][j+y])
            for k in range(1, 10):
                # check if they are in the same column or row
                if buf.count(str(k)) < 4 and buf.count(str(k)) > 1:
                    indices = []
                    for x in range(0, 3):
                        for y in range(0, 3):
                            if str(k) in pos[i+x][j+y]:
                                indices.append([i+x, j+y])
                    index = getColumnorRow(indices)
                    if index[0] == 0:
                        clearColumn(str(k), index[1], min(index[2]), max(index[2]), pos, npos)
                    elif index[0] == 1:
                        clearRow(str(k), index[1], min(index[2]), max(index[2]), pos, npos)
            j += 3
        i = i + 3


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


