import pygame as pg   
from .spritesheet import SpriteSheet

#Loading the spritesheet 
my_spritesheet = SpriteSheet("assets\\colored_packed.png")

tree = my_spritesheet.get_sprite(0 , 16 , 16 , 16)
rock = my_spritesheet.get_sprite(81 , 32 , 16 , 16)
grass = my_spritesheet.get_sprite(80 , 0 , 16 , 16)
dirt = my_spritesheet.get_sprite(64 , 0 , 16 , 16)
empty = my_spritesheet.get_sprite(0 , 0 , 16 , 16)
energy_pyramid = my_spritesheet.get_sprite( 35, 339 , 16 , 16)
target_mark = my_spritesheet.get_sprite(426 ,240 , 16 , 16)
scorpion = my_spritesheet.get_sprite(407 , 85 , 16 , 16)
tiny_guy = my_spritesheet.get_sprite(426 , 0 , 16 , 16)
