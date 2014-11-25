import random
import sudoku

LEVELS = [(50, 60), (36, 49), (32, 35), (28, 31), (22, 27)]

LOWERBOUNDS = [5, 4, 3, 2, 0]

def createFullPuzzle(board):
    for i in range(0, 9):
        for j in range(0, 9):
            tmp = ['1','2','3','4','5','6','7','8','9']
            while True:
                board[i][j] = random.choice(tmp)
                if sudoku.validateCell(board, i, j):
                    break 
                else:
                    tmp.remove(board[i][j])
                    if len(tmp) == 0:
                        sudoku.print_board(board)
                        return board
    sudoku.print_board(board)
    return board

def checkSolution(board1, board2):
    for i in range(0, 9):
        for j in range(0, 9):
            if board1[i][j] != board2[i][j]:
                return False
    return True

def generateBoard(difficulty=4):
    # generate a full puzzle, then remove the items to create different difficulty level
    board = [['0' for x in xrange(9)] for x in xrange(9)]
    while not sudoku.validateBoard(board):
        board = createFullPuzzle(board)
    
    sudoku.print_board(board)
    result = board
    lb = LEVELS[difficulty][0]
    ub = LEVELS[difficulty][1]
    num = LOWERBOUNDS[difficulty]

    removedCtr = 0
    while (81 - removedCtr) >= lb:
        i = random.randrange(0, 9)
        j = random.randrange(0, 9)
        if board[i][j] != '0':
            # check row
            if (9 - board[i].count('0')) > num:
                continue
            buf = []
            # check col
            for k in range(0, 9):
                buf.append(board[i][k])
            if (9 - buf.count('0')) > num:
                continue
            tmp = board[i][j]
            board[i][j] = '0'
            tmpboard = sudoku.solve(board)
            if checkSolution(tmpboard, result):
                removedCtr += 1
                if (81 - removedCtr) <= ub and random.randrange(0, 10) < 4:
                    break
            else:
                board[i][j] = tmp

    sudoku.print_board(board)
    sudoku.print_board(result)

def createPartialPuzzle(difficulty, board):
    lb = LEVELS[difficulty][0]
    ub = LEVELS[difficulty][1]
    num = LOWERBOUNDS[difficulty]

    placedCtr = 0
    while placedCtr <= ub:
        i = random.randrange(0, 9)
        j = random.randrange(0, 9)
        if board[i][j] == '0':
            tmp = ['1','2','3','4','5','6','7','8','9']
            while True:
                board[i][j] = random.choice(tmp)
                if sudoku.validateCell(board, i, j):
                    placedCtr += 1
                    if placedCtr >= lb and random.randrange(0, 10) < 4:
                        return board
                    break 
                else:
                    tmp.remove(board[i][j])
                    if len(tmp) == 0:
                        return board

def addElement(board):
    i = random.randrange(0, 9)
    j = random.randrange(0, 9)
    while board[i][j] != '0':
        i = random.randrange(0, 9)
        j = random.randrange(0, 9)
    while True:
        tmp = ['1','2','3','4','5','6','7','8','9']
        board[i][j] = random.choice(tmp)
        if sudoku.validateCell(board, i, j):
            return board
        else:
            tmp.remove(board[i][j])
            if len(tmp) == 0:
                return None

def generateBoard2(difficulty=4):
    board = [['0' for x in xrange(9)] for x in xrange(9)]
    LB = LEVELS[difficulty][0]
    UB = LEVELS[difficulty][1]

    placedCtr = 0
    while True:
        if placedCtr > UB:
            placedCtr = 0
            board = [['0' for x in xrange(9)] for x in xrange(9)]
        if addElement(board) != None:
            placedCtr += 1
            sudoku.print_board(board)
            result = sudoku.solve(board)
            if sudoku.checkIfDone(result):
                # there is a solution
                print "nyan"
                break
            else:
                print "delai"
                sudoku.print_board(result)
        else:
            placedCtr = 0
            board = [['0' for x in xrange(9)] for x in xrange(9)]
    sudoku.print_board(board)

generateBoard2(0)

