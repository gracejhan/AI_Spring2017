# -*- coding: utf-8 -*-
from __future__ import print_function
from time import time


class Solver(object):

    # This solver object takes gameboard state
    # bestMoveSearch f(x) uses search f(x) to find the solution
    # bestMoveRule f(x) uses rule f(x) to find the solution

    board = None
    colors = ["o", "x"]

    def __init__(self, board, color):

        self.board = [x[:] for x in board]
        self.AIcolor = color

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
            legal_moves = {3: 5, 2: 0, 4: 0, 1: 0, 5: 0, 0: -5, 6: -5}
        else:
            legal_moves = {3: 0, 2: 0, 4: 0, 1: 0, 5: 0, 0: 0, 6: 0}

        for column in columns:  # 0~6
            print("Searching column number : ", end="")
            print(column + 1)

            if not self.isLegalMove(column, board):
                legal_moves[column] = -9999999

            if self.isLegalMove(column, board) and time() - start < 100:
                temp = self.makeMove(board, column, currentPlayer)
                legal_moves[column] += -self.search(depth, -999, 999, temp, enemyPlayer)  # puts in the alpha values of each choice

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

        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(board):
            return self.value(board, currentPlayer)

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
        enemyConnectThree = self.checkForStreak(board, enemyTile, 3)
        enemyConnectTwo = self.checkForStreak(board, enemyTile, 2)

        result = (connectFour * 10000 + connectThree * 100 + connectTwo) - \
                 (enemyConnectFour * 10000 + enemyConnectThree * 100 + enemyConnectTwo)

        return result

    def removeDefaultRule(self, legal_moves, rule):
        temp_list = [v[rule] for k, v in legal_moves.items()]
        if 0 not in temp_list:
            for k, v in legal_moves.items():
                v[rule] = 0


    def removeRedundancyRule(self, legal_moves, rule):
        temp_list = [v[rule] for k, v in legal_moves.items()]
        if all(item == temp_list[0] for item in temp_list):
            for k, v in legal_moves.items():
                v[rule] = 0

                # if k == 0:
                #     v[rule] -= v[rule]
                #     v[rule+2] -= v[rule+2]+1
                #     v[rule+4] -= v[rule+4]+1
                # elif k == 2:
                #     v[rule] -= v[rule]
                #     v[rule+2] -= v[rule]+1
                # elif k == 4:
                #     v[rule] -= v[rule]



    def bestMoveRule(self, board, currentPlayer, phase):
 
        
        legal_moves = {}        # dictionary where keys: column numbers, values: a 8 number tuple which denotes the rules applied

        for column in range(7):  # iterate all columns
            if self.isLegalMove(column, board):
                selected_row, temp = self.make_move2(board, column, currentPlayer)
                legal_moves[column] = self.rule_checking_flags(temp, currentPlayer, selected_row, column)                # RULE BASED ALGORITHM

              #  temp2 = self.make_move_rulebased(temp, column, enemyPlayer, temp.local_point)   #depth 2
              #  legal_moves[column] = self.rule_enemy(temp2, enemyPlayer)

        # legal_moves[3] = [1, 1, 2, 4, 5, 1..])
        # {3: [1, 2,, 1],
        # 4: ...
        # 5}

        for rule_num in [1, 3, 5]:
            self.removeDefaultRule(legal_moves, rule_num)



        for rule_num in [0,2,4]:
            self.removeRedundancyRule(legal_moves,rule_num)


        get_value = lambda key: legal_moves[key]
        best_point = max(legal_moves, key=get_value)  # column값(key) 나옴

        print(best_point, legal_moves[best_point])

        messages = {
            0: "Rule 1: If there is a winning move, take it.",
            1: "Rule 2: Avoid the situation that the opponent can make a winning move.",
            2: "Rule 3: If my square can create or extend the streak, make it",
            3: "Rule 4: Avoid the situation that the opponent can connect 3.",
            4: "Rule 3: If my square can create or extend the streak, make it.",
            5: "Rule 5: Avoid the situation that the opponent can connect 2.",
            6: "Rule 6: Put the stone in a square at odd row (except for the first)",
            7: "Rule 7: Place a stone at center, or corner if not possible"
        }

        for rule in range(8):
            if legal_moves[best_point][rule]:
                print(messages[rule])



        return best_point

    def rule_checking_flags(self, board, currentPlayer, row, column):
        flag = [0] * 8
        if currentPlayer == self.colors[0]:
            enemyPlayer = self.colors[1]
        else:
            enemyPlayer = self.colors[0]

        connectFour = self.checkForStreak(board, currentPlayer, 4)
        connectThree = self.checkForStreak(board, currentPlayer, 3)
        connectTwo = self.checkForStreak(board, currentPlayer, 2)

        if connectFour:
            flag[0] += connectFour

        if connectThree:
            flag[2] += connectThree

        if connectTwo:
            flag[4] += connectTwo

        if row == 2 or row == 4:
            flag[6] += 1

        if column == 3 :
            flag[7] += 2
        elif column == 0 or column == 6:
            flag[7] += 1

        flag[1], flag[3], flag[5] = 1, 1, 1
        for column in range(7):
            if self.isLegalMove(column, board):
                _, temp_board = self.make_move2(board, column, enemyPlayer)

                rule_enemy_tuples = ((1, 4), (3, 3), (5,2))
                for rule, consecutive in rule_enemy_tuples:
                    if self.checkForStreak(temp_board, enemyPlayer, consecutive) != 0:
                        flag[rule] = 0

        return flag



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
                    continue
        return count

    def verticalCheck(self, row, column, board, streak):

        line = 0
        # color = board[row][column]

        # if row >0:
        #     if board[row-1][column] == color:
        #         return 0
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

        # color = board[row][column]
        #
        # if column > 0:
        #     if board[row][column-1] == color:
        #         return 0

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
        # line = 0
        # color = board[row][column]
        #
        # if row > 0 and column > 0:
        #     if board[row-1][column-1] == color:
        #         line = 0
        # else:
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

        # if row < 6 and column > 0:
        #     if board[row+1][column-1] == color:
        #         line = 0
        # else:
        line = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif board[i][j].lower() == board[row][column].lower():
                line += 1
            else:
                break
            j -= 1  # decrement column when row is incremented

        if line >= streak:
            total += 1

        return total
