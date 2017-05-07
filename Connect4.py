from __future__ import print_function
from Solver import Solver


class Game(object):

    board = None
    phase = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    colors = ["o", "x"]

    def __init__(self):
        self.phase = 1
        self.finished = False
        self.winner = None

        print("Do you go first or second?")

        while self.players[0] is None:

            choice = int(input("Type 1 or 2 : "))

            if choice == 1:
                self.players[0] = AIPlayer(self.colors[0])
                self.players[1] = Player(self.colors[1])

            elif choice == 2:
                self.players[0] = Player(self.colors[0])
                self.players[1] = AIPlayer(self.colors[1])

            else:
                print("Error, try again")

        print("Player 1 is {0}".format(self.colors[0]))
        print("Player 2 is {0}".format(self.colors[1]))

        self.turn = self.players[0]

        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def newGame(self):

        self.phase = 1
        self.finished = False
        self.winner = None
        self.turn = self.players[0]

        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        self.phase += 1

    def nextMove(self):
        player = self.turn

        if self.phase > 42:
            self.finished = True
            return

        move = player.move(self.board, self.phase)

        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        print("Invalid move")

        return

    def checkForFours(self):

        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return
                    if self.diagonalCheck(i, j):
                        self.finished = True
                        return

    def verticalCheck(self, row, column):

        connectFour = False
        line = 0

        for i in range(row, 6):
            if self.board[i][column].lower() == self.board[row][column].lower():
                line += 1
            else:
                break

        if line >= 4:
            connectFour = True
            if self.players[0].color.lower() == self.board[row][column].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return connectFour

    def horizontalCheck(self, row, column):

        connectFour = False
        line = 0

        for j in range(column, 7):
            if self.board[row][j].lower() == self.board[row][column].lower():
                line += 1
            else:
                break

        if line >= 4:
            connectFour = True
            if self.players[0].color.lower() == self.board[row][column].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return connectFour

    def diagonalCheck(self, row, column):

        connectFour = False
        count = 0
        line = 0

        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][column].lower():
                line += 1
            else:
                break
            j += 1

        if line >= 4:
            count += 1
            if self.players[0].color.lower() == self.board[row][column].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        line = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][column].lower():
                line += 1
            else:
                break
            j += 1

        if line >= 4:
            count += 1
            if self.players[0].color.lower() == self.board[row][column].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            connectFour = True

        if count == 2:
            return connectFour

    def printState(self):

        print("Phase: " + str(self.phase))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")


class Player(object):

    # player object

    type = None
    color = None

    def __init__(self, color):
        self.type = "Human"
        self.color = color

    def move(self, state, phase):
        print("Enemy is {0}".format(self.color))
        column = None
        while column is None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):

    depth = None

    def __init__(self, color, depth=6):
        self.type = "Computer"
        self.color = color
        self.depth = depth

    def move(self, board, phase):
        print("We are {0}".format(self.color))
        print("What solver will you choose? ")
        solveOption = int(input("Type 1 for Search and 2 for Rules : "))

        if solveOption == 1:
            print("Using search algorithm...")
            m = Solver(board)
            if phase <= 6:
                bestMove, value = m.bestMoveSearch(self.depth, board, self.color, phase)
            elif phase <= 16:
                bestMove, value = m.bestMoveSearch(self.depth + 1, board, self.color, phase)
            else:
                bestMove, value = m.bestMoveSearch(self.depth + 2, board, self.color, phase)
            return bestMove

        elif solveOption == 2:
            m = Solver(board)
            bestMove = m.bestMoveRule(board, self.color, phase)
            return bestMove

        else:
            print("Error, using search algorithm...")
            m = Solver(board)
            bestMove, value = m.bestMoveSearch(self.depth, board, self.color, phase)
            return bestMove


########################################################################


# Methods

"""
class game(object):
    def __init__(self):
        self.move = ''
        self.board = []
        self.nodeCount = 0
        self.numRow = 6
        self.numCol = 7
    def printBoard(self, board):
        print()
        print(' ', end='')
        for x in range(1, self.numCol + 1):
            print(' %s  ' % x, end='')
        print()
        print('+---+' + ('---+' * (self.numCol - 1)))
        for y in range(self.numRow):
            print('|   |' + ('   |' * (self.numCol - 1)))
            print('|', end='')
            for x in range(self.numCol):
                print(' %s |' % self.board[x][y], end='')
            print()
            print('|   |' + ('   |' * (self.numCol - 1)))
            print('+---+' + ('---+' * (self.numCol - 1)))
    def resetBoard(self):
        self.move = ''
        board = []
        for x in range(self.numCol):
            board.append([" "] * self.numRow)
        self.board = board
    def makeMyMove(self, column):
        for y in range(self.numRow - 1, -1, -1):
            if self.board[column][y] == ' ':
                self.board[column][y] = 'O'
                self.move = self.move + str(column + 1)
                return
    def makeEnemyMove(self, column):
        for y in range(self.numRow - 1, -1, -1):
            if self.board[column][y] == ' ':
                self.board[column][y] = 'X'
                self.move = self.move + str(column + 1)
                return
    def makeMoves(self, moves, goFirst):
        move = moves[0]
        move = int(move)
        if goFirst:
            self.makeMyMove(move - 1)
        else:
            self.makeEnemyMove(move - 1)
        if len(moves) > 1:
            moves = moves[1:]
            self.makeMoves(moves, not goFirst)
    def checkWin(self, tile):
        # check horizontal spaces
        for y in range(self.numRow):
            for x in range(self.numCol - 3):
                if self.board[x][y] == tile and self.board[x + 1][y] == tile and self.board[x + 2][y] == tile and self.board[x + 3][y] == tile:
                    return True
        # check vertical spaces
        for x in range(self.numCol):
            for y in range(self.numRow - 3):
                if self.board[x][y] == tile and self.board[x][y + 1] == tile and self.board[x][y + 2] == tile and self.board[x][y + 3] == tile:
                    return True
        # check / diagonal spaces
        for x in range(self.numCol - 3):
            for y in range(3, self.numRow):
                if self.board[x][y] == tile and self.board[x + 1][y - 1] == tile and self.board[x + 2][y - 2] == tile and self.board[x + 3][y - 3] == tile:
                    return True
        # check \ diagonal spaces
        for x in range(self.numCol - 3):
            for y in range(self.numRow - 3):
                if self.board[x][y] == tile and self.board[x + 1][y + 1] == tile and self.board[x + 2][y + 2] == tile and self.board[x + 3][y + 3] == tile:
                    return True
        return False
    def negamax(self, move, alpha, beta, myTurn):
        assert alpha < beta
        self.nodeCount += 1
        if len(move) == (self.numCol * self.numRow):
            return 0
        for x in range(self.numCol):
            if self.canPlay(x) and self.isWinningMove(x, myTurn):
                return (self.numCol * self.numRow + 1 - len(move)) / 2
        max = (self.numCol * self.numRow - 1 - len(move)) / 2
        if beta > max:
            beta = max
            if alpha >= beta:
                return beta
        for x in range(self.numCol):
            if self.canPlay(x):
                tempMove = game()
                tempMove = copy.deepcopy(self)
                if myTurn:
                    tempMove.makeEnemyMove(x - 1)
                else:
                    tempMove.makeMyMove(x - 1)
                nextMove = move + str(x + 1)
                score = -tempMove.negamax(nextMove, -beta, -alpha, not myTurn)
                if score >= beta:
                    print(x)
                    return score
                if score > alpha:
                    alpha = score
        return alpha
    def canPlay(self, column):
        if self.board[column][0] == ' ':
            return True
        else:
            return False
    def isWinningMove(self, column, myTurn):
        if myTurn:
            tile = 'O'
        else:
            tile = 'X'
        row = 0
        if not self.canPlay(column):
            return False
        for y in range(self.numRow - 1, -1, -1):
            if self.board[column][y] == ' ':
                row = y
                break
        # check horizontal spaces
        if column < 4:
            if self.board[column + 1][row] == tile and self.board[column + 2][row] == tile and self.board[column + 3][row] == tile:
                return True
        if column > 2:
            if self.board[column - 1][row] == tile and self.board[column - 2][row] == tile and self.board[column - 3][row] == tile:
                return True
        # check vertical spaces
        if row < 3:
            if self.board[column][row + 1] == tile and self.board[column][row + 2] == tile and self.board[column][row + 3] == tile:
                return True
        # check / diagonal spaces
        if column > 2 and row < 3:
            if self.board[column - 1][row + 1] == tile and self.board[column - 2][row + 2] == tile and self.board[column - 3][row + 3] == tile:
                return True
        # check \ diagonal spaces
        if column < 4 and row < 3:
            if self.board[column + 1][row + 1] == tile and self.board[column + 2][row + 2] == tile and self.board[column + 3][row + 3] == tile:
                return True
        return False
    def solveAlg(self, move):
        self.nodeCount = 0
        move = str(move)
        print("evaluation for : ", end="")
        print(move)
        return self.negamax(move, - (self.numRow * self.numCol) / 2, (self.numCol) * (self.numRow) / 2, True)
    def solveRule(self):
        return
"""
