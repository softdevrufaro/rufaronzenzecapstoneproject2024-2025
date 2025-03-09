from .MAPF_solvers import CBS , CBS_MA , icbs_complete
class oracle: 
    def __init__(self , world , agents , obstacle_library):
        self.world = world 
        self.agents = agents
        self.start_positions , self.goal_positions = self.fetch_start_and_goal_positions()
        self.obstacle_library = None
    
    def simplify_world_matrix(self):
        try:
            simple_matrix = []
            for x , row in enumerate(self.world):
                temp = []
                for y , col in enumerate(row):
                    if self.world[x][y][1] in self.obstacle_library:
                        temp.append(1)
                    else: 
                        temp.append(0)
                simple_matrix.append(temp)
            return simple_matrix
        except Exception as e: 
            print(f"Something went wrong ({e})")
    
    def fetch_start_and_goal_positions(self):
        try:
            start = []
            goal = []
            for agent in self.agents:
                start.append(agent.start)
                goal.append(agent.goal)
            
            return start , goal
        except Exception as e: 
            print(f"Something went wrong ({e})")