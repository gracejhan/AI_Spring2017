# -*- coding: utf-8 -*-
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

        self.newGame()

    def newGame(self):
        self.phase = 1
        self.finished = False
        self.winner = None
        self.players[0] = None

        print("Do you want to go first or second?")

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
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][column].lower():
                line += 1
            else:
                break
            j -= 1

        if line >= 4:
            count += 1
            if self.players[0].color.lower() == self.board[row][column].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
                
        if count > 0:
            return True
        return False

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

    def __init__(self, color, depth=5):
        self.type = "Computer"
        self.color = color
        self.depth = depth

    def move(self, board, phase):
        print("We are {0}".format(self.color))
        print("What solver will you choose? ")
        solveOption = int(input("Type 1 for Search and 2 for Rules : "))

        if solveOption == 1:
            print("Using search algorithm...")
            m = Solver(board, self.color)
            if phase <= 6:
                bestMove, value = m.bestMoveSearch(self.depth, board, self.color, phase)
            elif phase <= 16:
                bestMove, value = m.bestMoveSearch(self.depth + 1, board, self.color, phase)
            else:
                bestMove, value = m.bestMoveSearch(self.depth + 2, board, self.color, phase)
            return bestMove

        elif solveOption == 2:
            m = Solver(board, self.color)
            bestMove = m.bestMoveRule(board, self.color, phase)
            return bestMove

        else:
            print("Error, using search algorithm...")
            m = Solver(board, self. color)
            bestMove, value = m.bestMoveSearch(self.depth, board, self.color, phase)
            return bestMove
