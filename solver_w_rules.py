import random


class Solver(object):

    # This solver object takes gameboard state
    # bestMoveSearch f(x) uses search f(x) to find the solution
    # bestMoveRule f(x) uses rule f(x) to find the solution

    board = None
    colors = ["o", "x"]

    def __init__(self, board):

        self.board = [x[:] for x in board]

    def bestMoveSearch(self, depth, board, currentPlayer):

        # return the best column number and the corresponding alpha value using search (option 1)

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        legal_moves = {}

        for column in range(7):  # 0~6
            if self.isLegalMove(column, board):
                temp = self.makeMove(board, column, currentPlayer)
                legal_moves[column] = -self.search(depth, temp, enemyPlayer)  # puts in the alpha values of each choice

        best_alpha = -999999
        best_move = None

        moves = legal_moves.items()

        random.shuffle(list(moves))

        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, board, currentPlayer):

        # return the alpha value

        legal_moves = []
        for i in range(7):
            if self.isLegalMove(i, board):
                temp = self.makeMove(board, i, currentPlayer)
                legal_moves.append(temp)

        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(board):
            return self.value(board, currentPlayer)

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        alpha = -99999999

        for child in legal_moves:
            if child is None:
                print("No children")
            alpha = max(alpha, -self.search(depth - 1, child, enemyPlayer))
        return alpha

    def bestMoveRule(self, board, currentPlayer):

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]


        legal_moves = {}

        for column in range(7):  # 0~6
            if self.isLegalMove(column, board):
                temp = self.make_move_rulebased(board, column, currentPlayer, local_point=0)
                legal_moves[column] = self.rule(temp, currentPlayer)  # RULE BASED ALGORITHM

        best_point = -999999
        best_move = None

        moves = legal_moves.items()

        random.shuffle(list(moves))

        for move, point in moves:
            if point >= best_point:
                best_point = point
                best_move = move

        return best_move

    def rule(self, board, tile):

        # return the point value
        # MAKE THIS PART FOR RULE BASED DECISION MAKING

        if tile == self.colors[0]:
            enemyTile = self.colors[1]
        else:
            enemyTile = self.colors[0]

        point = 0

        connectFour = self.checkForStreak(board, tile, 4)
        connectThree = self.checkForStreak(board, tile, 3)
        connectTwo = self.checkForStreak(board, tile, 2)
        enemyConnectFour = self.checkForStreak(board, enemyTile, 4)
        enemyConnectThree = self.checkForStreak(board, enemyTile, 3)

        if connectFour or connectThree or connectTwo:
            point += connectFour * 10000
            point += connectThree * 1000
            point += connectTwo * 100

        if enemyConnectFour :
            point = point - 5000

        if enemyConnectThree:
            point = point - 1000


        # 새로 들어오는 점이 홀수 열이면 가산점,
        # 가운데 3번 가산점 > 0번 6번 > 나머지
        point = point + self.local_point


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

        temp = [x[:] for x in board]            #copy
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def make_move_rulebased(self, board, column, color, local_point):

        local_point = 0

        temp = [x[:] for x in board]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                if i%2 == 0:    #odd row advantage
                    local_point += 30
                if column == 4:
                    local_point += 50
                elif column == 0 or column == 6:
                    local_point += 40
                else:
                    local_point = 0
                return temp, local_point


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
