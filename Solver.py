from __future__ import print_function
from time import time


class Solver(object):

    # This solver object takes gameboard state
    # bestMoveSearch f(x) uses search f(x) to find the solution
    # bestMoveRule f(x) uses rule f(x) to find the solution

    board = None
    colors = ["o", "x"]

    def __init__(self, board):

        self.board = [x[:] for x in board]

    def bestMoveSearch(self, depth, board, currentPlayer, phase):

        # return the best column number and the corresponding alpha value using search (option 1)

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        currPhase = phase
        best_alpha = -999999
        best_move = None
        start = time()

        columns = [3, 2, 4, 1, 5, 0, 6]
        if currPhase <= 6:
            legal_moves = {3: -994, 2: -999, 4: -999, 1: -999, 5: -999, 0: -1004, 6: -1004}
        else:
            legal_moves = {3: -999, 2: -999, 4: -999, 1: -999, 5: -999, 0: -999, 6: -999}

        for column in columns:  # 0~6
            print("Searching column number : ", end="")
            print(column + 1)

            if not self.isLegalMove(column, board):
                legal_moves[column] = -9999999

            if self.isLegalMove(column, board) and time() - start < 100:
                temp = self.makeMove(board, column, currentPlayer)
                legal_moves[column] += -self.search(depth, -999999, 999999, temp, enemyPlayer)  # puts in the alpha values of each choice

            print("Alpha : ", end="")
            print(legal_moves.items())
            print("Time passed : ", end="")
            print(time() - start)
            if time() - start > 119:
                break

        for move, alpha in legal_moves.items():
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, alpha, beta, board, currentPlayer):

        # return the max value

        columns = [3, 2, 4, 1, 5, 0, 6]
        legal_moves = []

        for i in columns:
            if self.isLegalMove(i, board):
                temp = self.makeMove(board, i, currentPlayer)
                legal_moves.append(temp)

        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(board):
            return self.value(board, currentPlayer)

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        bestMoveValue = -9999999

        for child in legal_moves:
            if child is None:
                print("No children")
            currValue = -self.search(depth - 1, -beta, -alpha, child, enemyPlayer)
            bestMoveValue = max(bestMoveValue, currValue)
            alpha = max(alpha, currValue)
            if alpha >= beta:
                break
        return bestMoveValue

    def bestMoveRule(self, board, currentPlayer, phase):
        """
        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]
        """
        # currPhase = phase

        legal_moves = {}

        for column in range(7):  # 0~6
            if self.isLegalMove(column, board):
                temp = self.makeMove(board, column, currentPlayer)
                legal_moves[column] = self.rule(temp, currentPlayer)  # RULE BASED ALGORITHM

        best_point = -999999
        best_move = None

        moves = legal_moves.items()

        for move, point in moves:
            if point >= best_point:
                best_point = point
                best_move = move

        return best_move

    def rule(self, board, tile):

        # return the point value
        # MAKE THIS PART FOR RULE BASED DECISION MAKING
        """
        if tile == self.colors[0]:
            enemyTile = self.colors[1]
        else:
            enemyTile = self.colors[0]
        """
        point = 0

        connectFour = self.checkForStreak(board, tile, 4)

        point += connectFour * 10000000

        return point

    def isLegalMove(self, column, board):

        # return boolean value if the move is legal

        for i in range(6):  # 0-5
            if board[i][column] == ' ':
                return True
        return False

    def gameIsOver(self, board):
        if self.checkForStreak(board, self.colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(board, self.colors[1], 4) >= 1:
            return True
        else:
            return False

    def makeMove(self, board, column, color):

        # return a temporary state after the move is updated

        temp = [x[:] for x in board]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, board, tile):

        # evaluate the fitness of each board state for the player
        # connect4 = 10000 points, connect3 = 100 points, connect2 = 1 point
        # enemy point is minus points

        if tile == self.colors[0]:
            enemyTile = self.colors[1]
        else:
            enemyTile = self.colors[0]

        connectFour = self.checkForStreak(board, tile, 4)
        connectThree = self.checkForStreak(board, tile, 3)
        connectTwo = self.checkForStreak(board, tile, 2)
        enemyConnectFour = self.checkForStreak(board, enemyTile, 4)
        # enemyConnectThree = self.checkForStreak(board, enemyTile, 3)
        # enemyConnectTwo = self.checkForStreak(board, enemyTile, 2)

        if enemyConnectFour > 0:
            return -10000
        else:
            return connectFour * 10000 + connectThree * 100 + connectTwo

    def checkForStreak(self, board, tile, streak):

        # return the count of streaks

        count = 0

        for i in range(6):
            for j in range(7):

                if board[i][j].lower() == tile.lower():
                    # vertical check
                    count += self.verticalCheck(i, j, board, streak)
                    # horizontal check
                    count += self.horizontalCheck(i, j, board, streak)
                    # diagonal check /, \
                    count += self.diagonalCheck(i, j, board, streak)
        return count

    def verticalCheck(self, row, column, board, streak):

        line = 0

        for i in range(row, 6):
            if board[i][column].lower() == board[row][column].lower():
                line += 1
            else:
                break

        if line >= streak:
            return 1
        else:
            return 0

    def horizontalCheck(self, row, column, board, streak):

        line = 0

        for j in range(column, 7):
            if board[row][j].lower() == board[row][column].lower():
                line += 1
            else:
                break

        if line >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, column, board, streak):

        total = 0

        line = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif board[i][j].lower() == board[row][column].lower():
                line += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if line >= streak:
            total += 1

        line = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif board[i][j].lower() == board[row][column].lower():
                line += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if line >= streak:
            total += 1

        return total
