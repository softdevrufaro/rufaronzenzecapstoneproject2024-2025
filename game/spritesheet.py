import pygame as pg   

screen = pg.display.set_mode((0 , 0) , pg.FULLSCREEN)
class SpriteSheet:
    def __init__(self , filename ):
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert()

    def get_sprite(self , x , y , width , height):
        sprite = pg.Surface((width , height))
        sprite.set_colorkey((0 , 0 ,0))
        sprite.blit(self.spritesheet , (0 , 0) , (x , y, width , height))
        return sprite