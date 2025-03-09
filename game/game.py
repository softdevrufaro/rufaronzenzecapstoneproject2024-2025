import pygame as pg   
import sys 
from .world import World
class Game: 
    def __init__(self , screen , clock):
        self.screen = screen 
        self.clock = clock 
        self.width , self.height = self.screen.get_size()
        # Creating the world instance in the game class
        self.world = World(self.screen , 100 , 100 , self.width , self.height , 42)

    def run(self):
        self.playing = True
        while self.playing: 
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
    def update(self):
        pass

    def draw(self):
        self.screen.fill((0 , 0 , 0))
        self.world.display_world()
        self.world.map_mouse()
        pg.display.flip()