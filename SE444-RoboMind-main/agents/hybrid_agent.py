"""
Hybrid Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Integrate search + logic + probability
Phase 4 of the project (Week 7-8) - Final Integration
"""

from environment import GridWorld
from agents.search_agent import SearchAgent
from agents.logic_agent import LogicAgent
from agents.probabilistic_agent import ProbabilisticAgent
from ai_core.knowledge_base import KnowledgeBase
from ai_core.bayes_reasoning import bayes_update
from ai_core.bayes_reasoning import update_belief_map


class HybridAgent:
    """
    A rational agent that integrates search, logic, and probabilistic reasoning.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the hybrid agent."""
        self.env = environment
        
        # Search component
        self.search_agent = SearchAgent(environment)
        
        # Logic component
        self.kb = KnowledgeBase()
        self.logic_agent = LogicAgent(environment)
        
        # Probabilistic component - initialize belief map
        self.beliefs = {}
        for row in range(self.env.height):
            for col in range(self.env.width):
                self.beliefs[(row, col)] = 0.35  # Initial belief for each cell
        
        self.prob_agent = ProbabilisticAgent(environment)
        # Synchronize beliefs
        self.prob_agent.beliefs = self.beliefs
        
        # Track visited positions to avoid oscillation 
        self.visited_positions = set()
        self.last_position = None
        
    def perceive(self):
        # we need to gather some facts using the agent_pos from self.env
        # facts that we need to add to the KB is
        # AgentAt(r,c) current position of the agent
        # Free(r,c) for current position and if value is 0
        # Safe(r,c) for current position and if value is 0
        # Obstacle(r,c) if value is 1 
        # Facts about the neighbors of the agent current position
        # first we need to know the agent current position
        r,c = self.env.agent_pos

        sensor_reading = (self.env.grid[r][c] == 1) # 1. Sensor reading

    
        self.beliefs = update_belief_map(self.beliefs, sensor_reading) # 2. Update belief map using Bayes
        

        

        #using those position we can add those facts to KB
        self.kb.tell(f"AgentAt({r},{c})")
        self.kb.tell(f"Free({r},{c})")
        self.kb.tell(f"Safe({r},{c})")


       


        #alos we can add the rules
        self.kb.add_rule([f"Free({r},{c})"], f"Safe({r},{c})")
        self.kb.add_rule([f"Free({r},{c})",f"Safe({r},{c})"], f"CanMove({r},{c})")


        # now we need to get the neighbors of the current agent position
        # using get_neighbors(pos) from self.env
        neighbors = self.env.get_neighbors((r,c))

        
        for nr, nc in neighbors:
            cell = self.env.grid[nr][nc]

            #when the cell coordinate is actually the goal coordinate  
            if (nr, nc) == self.env.goal:
                self.kb.tell(f"Goal({nr},{nc})")
                self.kb.tell(f"Free({nr},{nc})")
                self.kb.tell(f"Safe({nr},{nc})")
                

                #add rules
                self.kb.add_rule([f"Free({nr},{nc})"],f"Safe({nr},{nc})")
                self.kb.add_rule([f"Free({nr},{nc})",f"Safe({nr},{nc})"],f"CanMove({nr},{nc})")
                self.kb.add_rule([f"Goal({nr},{nc})"],f"CanMove({nr},{nc})")

            # If neighbor is free space
            elif cell == 0:
                self.kb.tell(f"Free({nr},{nc})")
                self.kb.tell(f"Safe({nr},{nc})")

                #add rules
                self.kb.add_rule([f"Free({nr},{nc})"],f"Safe({nr},{nc})")
                self.kb.add_rule([f"Free({nr},{nc})",f"Safe({nr},{nc})"],f"CanMove({nr},{nc})")

            #when the cell is 1, then it is obstacle
            elif cell == 1:
                self.kb.tell(f"Obstacle({nr},{nc})")
                self.kb.tell(f"NotSafe({nr},{nc})")

                self.kb.add_rule([f"Obstacle({nr},{nc})"], f"NotSafe({nr},{nc})")
    
    def plan(self):
        """
        Use search algorithms to plan a path to the goal.
        Hybrid agent should call A* when it needs a global plan.
        """
        try:
            path, cost, expanded = self.search_agent.search("astar")
            # Store path for debugging or future use
            self.search_plan = path  
            return path
        except Exception as e:
            print(f"[HybridAgent] Search failed: {e}")
            return None
    
    def reason(self):
        """
        Use logic to infer safe moves and update knowledge base.
        """
        # here the agent tell the kb to make inference 
        # using the facts and rules has
        # Also we need to know what and how many facst are derived for deubging purpose
        facts_before = len(self.kb.facts)
        self.kb.infer()
        facts_after = len(self.kb.facts)
        derived_facts  = facts_after - facts_before
        print(f"{derived_facts} facts have been derived after the reasoning")
        #printing new facts
        if derived_facts > 0:
            print("New Facts: ")
            for fact in self.kb.facts:
                print(" -", fact) 

    
    def update_beliefs(self):
        """
        Use Bayesian inference to handle uncertain sensor readings.
        """
        r, c = self.env.agent_pos

        # getting sensor belief values for an obstacle
        sensor_reading = (self.env.grid[r][c] == 1)
        self.beliefs = update_belief_map(self.beliefs,sensor_reading)
    
    def act(self):
        """
        Integrate all reasoning techniques to decide next action.
        
        Strategy:
            1. If goal is visible and path is clear → use search
            2. If uncertain about obstacles → use probability
            3. If need to infer hidden info → use logic
        """
        r, c = self.env.agent_pos
        
        # Track visited positions
        self.visited_positions.add((r, c))
        
        # Check if we've reached the goal
        if (r, c) == self.env.goal:
            print(" Goal reached!") #For debugging
            return (r, c)
        
        # Get valid neighbors
        neighbors = self.env.get_neighbors((r, c))
        
        if not neighbors:
            print("Agent stuck")
            return (r, c)
        
        # Use logic to filter safe moves
        # Ask the knowledge base which neighbors are safe to move to
        logic_safe_moves = []
        for nr, nc in neighbors:
            if self.kb.ask(f"CanMove({nr},{nc})"):
                logic_safe_moves.append((nr, nc))
        
        print(f"[Logic] Found {len(logic_safe_moves)} safe moves: {logic_safe_moves}") 
        
        # Use search to find optimal path if we have safe moves
        if logic_safe_moves:
            # Update search agent's starting position to current position
            self.search_agent.current_pos = (r, c)
            original_start = self.env.start
            self.env.start = (r, c)  # Temporarily update environment start
            
            # Try to use A* to find the best path to goal
            try:
                path, cost, expanded = self.search_agent.search("astar")
                
                if path and len(path) > 1:
                    next_pos = path[1]  # path[0] is current position
                    
                    # Verify the next position from search is in our logic-safe moves
                    if next_pos in logic_safe_moves:
                        print(f"[Search] Following A* path to {next_pos}")
                        self.env.start = original_start  # Restore original start
                        self.last_position = (r, c)
                        return next_pos
                    else:
                        print(f"[Search] A* suggests {next_pos} but logic says unsafe")
                self.env.start = original_start  # Restore original start
            except Exception as e:
                print(f"[Search] Failed: {e}")
                self.env.start = original_start  # Restore original start
        
        # Use probability to choose safest uncertain move
        # If logic didn't give us safe moves or search failed, use probabilistic reasoning
        if not logic_safe_moves:
            print("[Probability] No logically safe moves, using belief map")
            
            # Use probabilistic agent's decision-making
            prob_choice = self.prob_agent.act()
            
            if prob_choice in neighbors:
                print(f"[Probability] Choosing {prob_choice} based on beliefs")
                self.last_position = (r, c)
                return prob_choice
        
        # Hybrid decision combine logic safety with probabilistic beliefs
        # Prefer unvisited neighbors, avoid going back to last position
        if logic_safe_moves:
            # Filter out the last position if we have alternatives
            candidates = []
            for pos in logic_safe_moves:
                if pos != self.last_position:
                    candidates.append(pos)
            if not candidates:
                candidates = logic_safe_moves
            
            # Prefer less-visited or unvisited cells
            best_move = min(
                candidates,
                key=lambda cell: (
                    1 if cell in self.visited_positions else 0,  # Prefer unvisited, so if the cell was visited it will have a value of one making it unlikely to be the min 
                    self.beliefs.get(cell, 0.5),  # Prefer lower obstacle probability
                    self.env.manhattan_distance(cell, self.env.goal)  # Then prefer closer to goal
                )
            )
            print(f"[Hybrid] Choosing {best_move} (logic safe + exploration)")
            self.last_position = (r, c)
            return best_move
        
        # STEP 5: Fallback - choose any neighbor with lowest belief
        print("[Fallback] Choosing neighbor with lowest obstacle belief")
        candidates = []
        for pos in logic_safe_moves:
            if pos != self.last_position:
                candidates.append(pos)
        if not candidates:
            candidates = neighbors
            
        fallback_move = min(
            candidates,
            key=lambda cell: (
                self.beliefs.get(cell, 0.5),
                self.env.manhattan_distance(cell, self.env.goal)
            )
        )
        self.last_position = (r, c)
        return fallback_move




# Example usage
if __name__ == "__main__":
    print("Hybrid Agent - combines Search + Logic + Probability")
    print("This is the final phase - integrate everything!")

