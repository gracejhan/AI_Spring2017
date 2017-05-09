from __future__ import print_function
import sys
from Connect4 import *


def main():

    g = Game()
    g.printState()

    while True:
        while not g.finished:
            g.nextMove()

        g.printState()

        while True:
            play_again = int(input("Would you like to play again? 1 for Yes, 2 for No : "))

            if play_again == 1:
                g.newGame()
                g.printState()
                break

            elif play_again == 2:
                print("Thanks for playing!")
                sys.exit()

            else:
                print("I don't understand... ")

########################################################################


if __name__ == '__main__':
    main()
