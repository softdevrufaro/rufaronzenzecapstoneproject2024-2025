from .MAPF_solvers import CBS , CBS_MA , icbs_complete
class oracle: 
    def __init__(self , world , agents , obstacle_library):
        self.world = world 
        self.agents = agents
        self.obstacle_library = obstacle_library
        self.cbs_solution , self.cbs_ma_solution , self.icbs_solution = self.get_solver_solutions()
        self.best_solver = self.get_optimal_solver()

    
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
    
    def get_solver_solutions(self):
        world_simplified = self.simplify_world_matrix()
        starts , goals = self.fetch_start_and_goal_positions()
        # Initializing the solvers below
        cbs_solver = CBS.CBSSolver(world_simplified , starts , goals)
        cbs_ma_solver = CBS_MA.CBS_MASolver(world_simplified , starts , goals)
        icbs_solver = icbs_complete.ICBS_Solver(world_simplified , starts , goals)
        # fetching the solutions
        cbs_solution , cbs_num , cbs_expansion = cbs_solver.find_solution(disjoint=False)
        cbs_ma_solution , cbs_ma_num , cbs_ma_expansion = cbs_ma_solver.find_solution(disjoint=False)
        icbs_solution, icbs_num , icbs_expansion = icbs_solver.find_solution(disjoint=False)

        return cbs_solution , cbs_ma_solution , icbs_solution
    
    def get_optimal_solver(self):
        cbs_solution_score = 0
        for path in self.cbs_solution: 
            cbs_solution_score += len(path)
        cbs_ma_solution_score = 0
        for path in self.cbs_ma_solution: 
            cbs_ma_solution_score += len(path)
        icbs_solution_score = 0
        for path in self.icbs_solution:
            icbs_solution_score += len(path)
        
        solution_dictionary = {
            cbs_solution_score:"cbs",
            cbs_ma_solution_score:"cbs_ma",
            icbs_solution_score:"icbs"
        }

        list_of_scores = [cbs_solution_score , cbs_ma_solution_score,icbs_solution_score]
        best_score = min(list_of_scores)
        return solution_dictionary[best_score]
        

        
        
