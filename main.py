import pygame as pg    
import sys
from game.game import Game
# The main function that will run in the application

def main():
    # The running variable will control whether the application continues running or stops 
    # The playing variable will be used to pause or play the game

    running = True 
    playing = True 

    pg.init()
    pg.mixer.init()
    # The screen for the start of the game will be a full screen game
    screen = pg.display.set_mode((0 , 0) , pg.FULLSCREEN)
    # The game clock
    clock = pg.time.Clock()

    # Implement a menu

    #Implement a game
    game = Game(screen , clock)
    while running: 
        game.run()

if __name__ == "__main__":
    main()

