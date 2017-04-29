from __future__ import print_function
import sys
import copy

########################################################################


# Methods


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
        move = str(move)
        print("evaluation for : ", end = "")
        print(move)
        return self.negamax(move, - (self.numRow * self.numCol) / 2, (self.numCol) * (self.numRow) / 2, True)

    def solveRule(self):
        return


########################################################################


# Main


def main():

    while True:
        print("")
        print("CONNECT 4 SOLVER (6 x 7)")
        print("0. Reset Game")
        print("1. Solve using Search Algorithm")
        print("2. Solve using Rules")
        print("3. Input Enemy Move")
        print("4. Input My Move")
        print("5. Input Moves")
        print("6. Print Board")
        print("9. Quit")
        sel = input("Select Menu: ")

        if sel == 9:
            print("")
            print("Exiting...")
            sys.exit()

        elif sel == 0:
            print("")
            print("Initializing...")

            currentGame = game()

            # Reset Game
            currentGame.resetBoard()
            gameBoard = currentGame.board
            currentGame.printBoard(gameBoard)

            print("===== R E S U L T S =====")
            print("Possible moves: ", end="")

        elif sel == 1:

            print("")
            print("===== R E S U L T S =====")

            evaluation = currentGame.solveAlg(currentGame.move)
            print(evaluation)

        elif sel == 2:

            # Do Something

            print("")
            print("===== R E S U L T S =====")

        elif sel == 3:

            enemyColumn = input("What column did the enemy choose:")
            move = enemyColumn - 1

            if currentGame.isWinningMove(move, False):
                print("Looks like enemy has a winning move")

            currentGame.makeEnemyMove(move)
            currentGame.printBoard(gameBoard)
            print(currentGame.move)

            if currentGame.checkWin('X'):
                print("Enemy Wins!")

        elif sel == 4:

            myColumn = input("What column did you choose:")
            move = myColumn - 1

            if currentGame.isWinningMove(move, True):
                print("Looks like you have a winning move")

            currentGame.makeMyMove(move)
            currentGame.printBoard(gameBoard)
            print(currentGame.move)

            if currentGame.checkWin('O'):
                print("You Win!")

        elif sel == 5:

            currentGame = game()

            # Reset Game
            currentGame.resetBoard()
            gameBoard = currentGame.board

            goFirst = input("Did you go first? 1 for yes, 2 for no: ")
            if goFirst == 1:
                goFirst = True
            else:
                goFirst = False

            moves = input("Input the move sequence:")
            strMove = str(moves)

            currentGame.makeMoves(strMove, goFirst)

            print("")
            currentGame.printBoard(gameBoard)

        elif sel == 6:

            currentGame.printBoard(gameBoard)

########################################################################


if __name__ == '__main__':
    main()
