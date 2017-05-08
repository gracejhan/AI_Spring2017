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

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        currPhase = phase

        legal_moves = {}        #dictionary

        for column in range(7):  # 0~6
            if self.isLegalMove(column, board):
                selected_row, temp = self.make_move2(board, column, currentPlayer)
                legal_moves[column] = self.rule_checking_flags(temp, currentPlayer, selected_row, column)                # RULE BASED ALGORITHM

              #  temp2 = self.make_move_rulebased(temp, column, enemyPlayer, temp.local_point)   #depth 2
              #  legal_moves[column] = self.rule_enemy(temp2, enemyPlayer)

        # legal_moves[3] = [1, 1, 2, 4, 5, 1..])
        # {3: (board1, [1, 2,, 1]),
        # 4: ...
        # 5}

        get_value = lambda key: legal_moves[key]
        best_point = max(legal_moves, key=get_value) #column값 나옴
        best_move, _ = self.make_move2(board, best_point, currentPlayer)

        messages = {
            0: "Rule 1: If there is a winning move, take it.",
            1: "Rule 2: If the opponent can make winning move, interfere it.",
            2: "Rule 3: If my square can be connected for 3, make it.",
            3: "Rule 4: If the opponent can connect 3, interfere it.",
            4: "Rule 5: If my square can be connected for 2, make it.",
            5: "Rule 6: If the opponent can connect 2, interfere it.",
            6: "Rule 7: Put the stone in a square at odd row.",
            7: "Rule 8: Place a stone at center, or corner if not possible"
        }

        for rule in range(8):
            if legal_moves[best_point][rule]:
                print(messages[rule])


        #best_move = None

        # moves = legal_moves.items()

        # for move, point in moves:
        #     if point >= best_point:
        #         best_point = point
        #         best_move = move
        #

        return best_move

    def rule_checking_flags(self, board, tile, row, column):
        flag =[0]*8
        if tile == self.colors[0]:
            enemyTile = self.colors[1]
        else:
            enemyTile = self.colors[0]

        connectFour = self.checkForStreak(board, tile, 4)
        connectThree = self.checkForStreak(board, tile, 3)
        connectTwo = self.checkForStreak(board, tile, 2)

        if connectFour:
            flag[0] += 1

        if connectThree:
            flag[2] += 1

        if connectTwo:
            flag[4] += 1

        if row % 2 == 0 :
            flag[6] += 1

        if column == 3 :
            flag[7] += 2
        elif column == 0 or 6:
            flag[7] += 1

        flag[1], flag[3], flag[5] = 1, 1, 1
        for i in range(7):
            _, temp_board = self.make_move2(board, column, enemyTile)
            rule_enemy_tuples = ((1, 4), (3, 3), (5,2))
            for rule, opponent in rule_enemy_tuples:
                if self.checkForStreak(board, enemyTile, opponent):
                    flag[rule] = 0
            # enemyconnectFour = sef.checkForStreak(board, enemyTile, 4)
            # enemyconnectThree = self.checkForStreak(board, enemyTile, 3)
            # enemyconnectTwo = self.checkForStreak(board, enemyTile, 2)
        return flag


    # def rule_myself(self, board, tile):
    #
    #     # return the point value
    #     # MAKE THIS PART FOR RULE BASED DECISION MAKING
    #
    #     if tile == self.colors[0]:
    #         enemyTile = self.colors[1]
    #     else:
    #         enemyTile = self.colors[0]
    #
    #     connectFour = self.checkForStreak(board, tile, 4)
    #     connectThree = self.checkForStreak(board, tile, 3)
    #     connectTwo = self.checkForStreak(board, tile, 2)
    #     enemyConnectFour = self.checkForStreak(board, enemyTile, 4)
    #     enemyConnectThree = self.checkForStreak(board, enemyTile, 3)
    #
    #     if connectFour:
    #         self.flag_list[0] += 1
    #
    #     if connectThree:
    #         self.flag_list[2] += 1
    #
    #     if connectTwo:
    #         self.flag_list[5] += 1
    #
    #
    #
    #   ##  if enemyConnectFour :       #수정 필요, depth =2까지 봐야 구현 가능할듯
    #   ##      point = point - 5000
    #
    #   ##  if enemyConnectThree:
    #   ##      point = point - 1000
    #
    #
    #     # 새로 들어오는 점이 홀수 열이면 가산점,
    #     # 가운데 3번 가산점 > 0번 6번 > 나머지
    #    point = point + self.local_point
    #
    #
    #     return point

    # def rule_enemy(self, board, tile):
    #
    #     # return the point value
    #     # MAKE THIS PART FOR RULE BASED DECISION MAKING
    #
    #     if tile == self.colors[0]:
    #         currentPlayer = self.colors[1]
    #     else:
    #         currentPlayer = self.colors[0]
    #
    #     point = self.point
    #
    #     enemy_connectFour = self.checkForStreak(board, tile, 4)       #여기에 board라고 해도 맞는건가
    #
    #     if enemy_connectFour:
    #         point = point - 999999      # 점수 수정 필요
    #
    #
    #
    #     return point



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

    def make_move2(self, board, column, color):
        temp = [x[:] for x in board]
        for row in range(6):
            if temp[row][column] == ' ':
                temp[row][column] = color
                return row, temp



    # def make_move_rulebased(self, board, column, color):   #한 행에 대해 추가한 보드판
    #
    #
    #     flag = [0]*8
    #
    #     temp = [x[:] for x in board]
    #     for i in range(6):
    #         if temp[i][column] == ' ':
    #             temp[i][column] = color
    #
    #             if i%2 == 0:    #odd row advantage
    #                 flag[6] += 1
    #
    #             if column == 4:
    #                 flag[7] += 2
    #             elif column == 0 or column == 6:
    #                 flag[7] += 1
    #
    #
    #             return temp, flag

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

                if board[i][j] == tile:
                    # vertical check
                    count += self.verticalCheck(i, j, board, streak)
                    # horizontal check
                    count += self.horizontalCheck(i, j, board, streak)
                    # diagonal check /, \
                    count += self.diagonalCheck(i, j, board, streak)
                else:
                    return count
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
