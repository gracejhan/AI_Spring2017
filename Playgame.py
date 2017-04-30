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
            play_again = str(input("Would you like to play again? "))

            if play_again.lower() == 'y' or play_again.lower() == 'yes':
                g.newGame()
                g.printState()
                break
            elif play_again.lower() == 'n' or play_again.lower() == 'no':
                print("Thanks for playing!")
                sys.exit()

            else:
                print("I don't understand... ")

########################################################################


if __name__ == '__main__':
    main()
