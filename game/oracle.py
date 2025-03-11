from MAPF_solvers.a_star_class import A_Star, get_location, get_sum_of_cost, compute_heuristics
from MAPF_solvers.CBS import CBSSolver
from MAPF_solvers.CBS_MA import CBS_MASolver
from MAPF_solvers.icbs_complete import ICBS_Solver
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
        start = []
        goal = []
        for agent in self.agents:
            start.append(agent.position)
            goal.append(agent.end_position)
            
        return start , goal
    
    def get_solver_solutions(self):
        world_simplified = self.simplify_world_matrix()
        starts , goals = self.fetch_start_and_goal_positions()
        # Initializing the solvers below
        cbs_solver = CBSSolver(world_simplified , starts , goals)
        cbs_ma_solver = CBS_MASolver(world_simplified , starts , goals)
        icbs_solver = ICBS_Solver(world_simplified , starts , goals)
        # fetching the solutions
        cbs_solution , cbs_num , cbs_expansion = cbs_solver.find_solution(disjoint=True)
        cbs_ma_solution , cbs_ma_num , cbs_ma_expansion = cbs_ma_solver.find_solution(disjoint=True)
        icbs_solution, icbs_num , icbs_expansion = icbs_solver.find_solution(disjoint=True)

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
        return list_of_scores
        

        
        
