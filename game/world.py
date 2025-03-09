import pygame as pg   
from .settings import TILE_SIZE, red , green , blue
import random
from .sprites import tree , rock , dirt , grass , empty
import noise 
import networkx as nx 
from .graph_controller import graph_controller

class World: 

    # The init method will take the size of the grid and the width and height of the screen
    def __init__(self , screen , grid_length_x , grid_length_y , width , height , seed ):
        self.screen = screen
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width 
        self.height = height
        self.seed = seed
        self.world , self.origin = self.generate_world()
        self.graph_controller =graph_controller(self.world , [tree , rock])
        
    # Function to initialize the world variable 
    def generate_world(self ):
        world = []
        for x in range(self.grid_length_x):
            temp = []
            for y in range(self.grid_length_y):
                # Code to generate noise here 
                determinant = self.fetch_noise(x , y , 10 , 6 , 0.2 , 1.5 , self.seed)
                space_sprite = None
                if 0 < determinant <= 0.4:
                    space_sprite = tree
                elif 0.4 < determinant <= 0.8:
                    space_sprite = empty
                elif 0.8 < determinant <= 1.0:
                    space_sprite = rock
                temp.append( [(x , y),space_sprite])# The co-ordinates on the grid and the value of noise
            world.append(temp)

        origin = [0 , 0]
        origin[0] = (self.width//2) - ((self.grid_length_x * TILE_SIZE)//2)
        origin[1] = (self.height//2) - ((self.grid_length_y * TILE_SIZE)//2)

        return world , origin
    
    #Function to fetch the noise for world generation
    def fetch_noise(self , x , y , SCALE , OCTAVES , PERSISTENCE , LACUNARITY , SEED ):
        noise_val = noise.snoise2(x/SCALE,
                                  y/SCALE, 
                                  octaves = OCTAVES , 
                                  persistence = PERSISTENCE ,
                                  lacunarity = LACUNARITY , 
                                  base = SEED)
        
        _noise_ = (noise_val + 1)/2
        return _noise_
    
    # This function will draw the tiles
    def draw_tile(self , x , y):
        # Below is the square variable for the game
        sq = (x , y, TILE_SIZE , TILE_SIZE)
        pg.draw.rect(self.screen , green , sq , 1)
            
    
    # This function will be the one to draw the world
    def display_world(self):
        for x , row in enumerate(self.world): 
            for y ,col in enumerate(row):
                sprite = self.world[x][y][1]
                self.screen.blit(sprite, (x*TILE_SIZE + self.origin[0] , y*TILE_SIZE + self.origin[1]))
    
    # This function will map the mouse to the game world
    def map_mouse(self):
        mouse_x , mouse_y = pg.mouse.get_pos()
        in_x_space = (self.origin[0] < mouse_x <= self.origin[0]+(self.grid_length_x * TILE_SIZE))
        in_y_space = (self.origin[1] < mouse_y <= self.origin[1]+(self.grid_length_y * TILE_SIZE))

        #Checking to see if the mouse is in the necessary grid space
        if in_x_space and in_y_space:
            # translating the cursor position onto the grid for cursor tracking
            cursor_pos = [0 , 0]

            cursor_pos[0] = mouse_x - self.origin[0]
            cursor_pos[1] = mouse_y - self.origin[1]

            cursor_pos[0] = cursor_pos[0]//TILE_SIZE
            cursor_pos[1] = cursor_pos[1]//TILE_SIZE

            sq = (cursor_pos[0]*TILE_SIZE + self.origin[0] + 1 , cursor_pos[1]* TILE_SIZE + self.origin[1] + 1 , TILE_SIZE -2 , TILE_SIZE  - 2)
            pg.draw.rect(self.screen , red , sq , 1)
    
    # This function will map the 2d Grid to a graph datastructure
    def translate_world_to_graph(self):
        # Declare the graph variable 
        world_graph = nx.Graph()
        # Adding the nodes and the edges to the graph
        for x , row in enumerate(self.world):
            for y , col in enumerate(row):
                # connecting the nodes above and below
                if x != len(self.world) - 1: 
                    world_graph.add_edge(self.world[x][y][0] , self.world[x+1][y][0] , weight = 1)
                # Connecting the nodes left to right 
                if y != len(row)-1:
                    world_graph.add_edge(self.world[x][y][0] , self.world[x][y+1][0] , weight = 1)
                #Connecting the nodes diagonally from left to right going down
                if (x!= len(self.world)-1) and (y != len(row)-1):
                    world_graph.add_edge(self.world[x][y][0] , self.world[x+1][y+1][0] , weight = 1.21)
                # Connecting the nodes diagonally from right to left going up 
                if (x != 0) and (y != len(row)-1):
                    world_graph.add_edge(self.world[x][y][0] , self.world[x-1][y+1][0] , weight = 1.21)
        """
        # Checking to see that the code is working with no bugs or errors
        for row in self.world: 
            for col in row: 
                neighbors = list(world_graph.neighbors(col[0]))
                print(f"Neighbors of node {col[0]}: {neighbors} : {len(neighbors)}")
        """
