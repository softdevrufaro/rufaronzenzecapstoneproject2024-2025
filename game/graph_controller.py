import networkx as nx
# world to graph 
class graph_controller: 
    def __init__(self , world , obstacle_library):
        self.world = world
        self.graph_object = self.convert_grid_to_graph()
        self.world_size = (len(world) , len(world[0]))
        self.obstacle_library = obstacle_library
        self.obstacles = self.fetch_obstacles()
    
    def convert_grid_to_graph(self):
        """
        This function will create convert the 2d grid to a graph and return the graph.
        The 2d grid object will be provided on the creation of the graph controller instance

        Returns: 
        graph: The value that will be returned will be a graph object version of the grid
        """
        try: 
            world = self.world
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
            obstacles = self.fetch_obstacles()
            G = self.disconnect_obstacles(obstacles=obstacles, G=G)
            return G
        except Exception as e: 
            print(f"Something went wrong [{e}]")
            return None
    
    def disconnect_obstacles(self , obstacles , G):
        """
        This function will remove all the obstacles in the world grid from the graph
        This will make it impossible for pathfinding algorithms to recognize an obstacle as a 
        potential path 
        
        Returns: 
        None : It will immediately update the controllers graph object."""
        world = G
        try: 
            for obstacle in obstacles:
                target_edges = list(world.edges(obstacle))
                world.remove_edges_from(target_edges)
            return world
        except Exception as e : 
            print(f"Sorry something went wrong({e})")
            return world
    
    # The code for fetching all the needed obstacles in the graph controller object
    def fetch_obstacles(self):
        """
        This function will search for all the obstacles in the world grid and then return all of them. 

        Args:
            G(graph): This graph object will server as the world and is the one from where we will remove the edges and nodes in the graph.
        Returns: 
        list: A list of all the nodes regarded as obstacles.
        """
        world = self.world
        obstacles = []
        for x , row in enumerate(self.world):
            for y , col in enumerate(row):
                if world[x][y][1] in self.obstacle_library:
                    obstacles.append(world[x][y][0])
        return obstacles
