from environment import GridWorld
from ai_core.bayes_reasoning import bayes_update
from ai_core.bayes_reasoning import update_belief_map # Imported from bayes_reasoning.py file


class ProbabilisticAgent:
    """
    An agent that uses Bayesian reasoning to handle uncertainty.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the probabilistic agent."""
        self.env = environment
        self.beliefs = {}  # Belief map: position -> probability
        for row in range(self.env.height):
            for column in range(self.env.width):
                self.beliefs[(row, column)] = 0.35 # Assumed initial belief
        self.last_pos = None
        
    def update_beliefs(self, sensor_reading, position):
        """Update beliefs using Bayes' rule."""
        self.beliefs = update_belief_map(self.beliefs,sensor_reading)
    
    def act(self):
        """Decide action based on probabilistic beliefs."""
        position = self.env.agent_pos # Get current position
        neighbors = self.env.get_neighbors(position) # Get valid neighbors
        if not neighbors:
            return position # To handle dead end cases
        
        candidates = [] # This will store potential available cells the agent can go to
        for n in neighbors:
            if n != self.last_pos: 
                # this avoids the case where the agent always selects the safest cell without thinking which could be the last cell
                # So it wouldnt oscillate  
                candidates.append(n)

        if not candidates:
            candidates = neighbors 
        # ^ The code above idea is to avoid immediate backtracking to the last position if there are alternatives
        # This happened to us lol

        # Chooses the safest neighbor (Lowest belief to obstacle)
        safest_cell = min(
            candidates,
            key=lambda cell: (self.beliefs.get(cell, 0.5), self.env.manhattan_distance(cell, self.env.goal))
        )
        self.last_pos = position
        return safest_cell