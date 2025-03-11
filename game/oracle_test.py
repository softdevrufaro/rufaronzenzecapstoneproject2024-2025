import time as timer
import pygame as pg   
import sys 
import random 
import networkx as nx 
import math
import oracle


pg.init()
pg.mixer.init()
screen = pg.display.set_mode((0 , 0) , pg.FULLSCREEN)
# Declaring the row and column variables 
row = 20
col = 20

world = []

for x in range(row) : 
    temp = []
    for y in range(col) : 
        temp.append([(x , y), 0])
    world.append(temp)

# Declaring the world graph and its nodes 
G = nx.Graph()
for x , row in enumerate(world):
    for y , col in enumerate(row):
        # Connecting the nodes above and below 
        if x != len(world)-1:
            G.add_edge(world[x][y][0] , world[x+1][y][0] , weight = 1)
        # Connecting the nodes diagonally from left to right
        if y != len(row)-1:
            G.add_edge(world[x][y][0] ,world[x][y+1][0] , weight = 1  )
        # Connecting the nodes diagonally from left to right goind down
        if (x != len(world)-1) and (y != len(row)-1):
            G.add_edge(world[x][y][0] , world[x+1][y+1][0] , weight =1.21 )
        # Connecting the nodes diagonally from right to left going up 
        if (x != 0) and (y != len(row)-1):
            G.add_edge(world[x][y][0] , world[x-1][y+1][0] , weight = 1.21)

obstacles = []

for a in range(100):
    repeat = True 
    while repeat: 
        x = random.randint( 0 , len(world) - 1 )
        y = random.randint( 0 , len(world) - 1 )
        repeat = world[x][y][0] in obstacles
    world[x][y][1] = 1
    obstacles.append(world[x][y][0])# Adding the obstacles to an obstacle list

unoccupied_space = []
for x , row in enumerate(world):
    for y , col in enumerate(row): 
        if world[x][y][0] in obstacles: 
            pass
        else:
            unoccupied_space.append(world[x][y][0])

new_2D_grid_map = []
for x in range(5):
    temp = []
    for y in range(5):
        if world[x][y][0] in obstacles: 
            temp.append(1)
        else:
            temp.append(0)
    new_2D_grid_map.append(temp)
        
class agent:
    def __init__(self , index , start , end_position):
        self.path = []
        self.id = index
        self.color = (255 / (index+1) , 0 , 0)
        self.position = start
        self.end_position = end_position
agents = []

for i in range(10):
    repeat = True 
    while repeat:
        repeat = False 
        x = random.randint( 0 , len(world)-1)
        y = random.randint(0 , len(world[0]) - 1)
        if world[x][y][0] in obstacles: 
            repeat = True 
        else:
            obstacles.append(world[x][y][0])
            new_agent = agent(i , world[x][y][0] , [0 , 0])
            agents.append(new_agent)

print(type(agents))
for my_agent in agents:
    repeat = True 
    while repeat: 
        repeat = False
        x = random.randint( 0 , len(world)-1)
        y = random.randint( 0 , len(world[0]) - 1)
        if world[x][y][0] in obstacles:
            repeat = True 
        else:
            obstacles.append(world[x][y][0])
            my_agent.end_position = world[x][y][0]

my_oracle = oracle.oracle(world , agents , [1])
best_solver  = my_oracle.get_optimal_solver()
print(best_solver[0])
print(best_solver[1])
print(best_solver[2])
agents = my_oracle.agents
def main():
    running = True 
    last_time = timer.time()
    while running : 
        current_time = timer.time()
        if current_time - last_time >= 1:
            for agent in agents: 
                if len(agent.path) >=1 : 
                    agent.position = agent.path.pop(0)
                else: 
                    pass
            last_time = current_time
        screen.fill((0 , 0 , 0))
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
        for x , row in enumerate(world):
            for y, col in enumerate(row):
                sq = (x*20 , y*20 , 20 , 20)
                if world[x][y][1] == 1: 
                    pg.draw.rect(screen , (0 , 255 , 0) , sq)
                else: 
                    pg.draw.rect(screen , (255 , 255 , 255) , sq , 1)
        for space in unoccupied_space:
            sq = (space[0] * 20 , space[1]*20 , 20 , 20)
            pg.draw.rect(screen , (0 , 0 , 255) ,sq , 2 )
        for agent in agents:
            sq = (agent.position[0]*20 , agent.position[1]*20 , 20 , 20)
            pg.draw.rect(screen , (agent.color) , sq )
        mouse_x , mouse_y = pg.mouse.get_pos()
        cursor_pos = [0 , 0]
        cursor_pos[0] = mouse_x//20
        cursor_pos[1] = mouse_y//20
        sq = (cursor_pos[0]*20, cursor_pos[1]*20 , 20 , 20 )
        pg.draw.rect(screen , (0 , 0 , 255) , sq , 2)
        pg.display.flip()
        pass

main()
