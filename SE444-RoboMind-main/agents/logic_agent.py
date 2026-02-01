"""
Logic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Implement logic-based reasoning agent
Phase 2 of the project (Week 3-4)
"""

from environment import GridWorld
from ai_core.knowledge_base import KnowledgeBase


class LogicAgent:
    """
    An agent that uses propositional logic to reason about the world.
    """
    
    def __init__(self, environment: GridWorld):
        """Initialize the logic agent."""
        self.env = environment
        self.kb = KnowledgeBase()
        
    def perceive(self):
        """Perceive the environment and update knowledge base."""
        # TODO: Implement

        # we need to gather some facts using the agent_pos from self.env
        # facts that we need to add to the KB is
        # AgentAt(r,c) current position of the agent
        # Free(r,c) for current position and if value is 0
        # Safe(r,c) for current position and if value is 0
        # Obstacle(r,c) if value is 1 
        # Facts about the neighbors of the agent current position
        # first we need to know the agent current position
        r,c = self.env.agent_pos
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
        # loop through all neighbors to know there status
        #  and add the facts about them
        for nr, nc in neighbors:
            # check the neighbor status using grid
            cell = self.env.grid[nr][nc]

            #when the cell coordinate is actually the goal coordinate  
            if (nr, nc) == self.env.goal:
                #add facts
                self.kb.tell(f"Goal({nr},{nc})")
                self.kb.tell(f"Free({nr},{nc})")
                self.kb.tell(f"Safe({nr},{nc})")
                

                #add rules
                self.kb.add_rule([f"Free({nr},{nc})"],f"Safe({nr},{nc})")
                self.kb.add_rule([f"Free({nr},{nc})",f"Safe({nr},{nc})"],f"CanMove({nr},{nc})")
                self.kb.add_rule([f"Goal({nr},{nc})"],f"CanMove({nr},{nc})")

            # when ever the cell is 0, then this cell is safe and free
            elif cell == 0:
                #add facts
                self.kb.tell(f"Free({nr},{nc})")
                self.kb.tell(f"Safe({nr},{nc})")

                #add rules
                self.kb.add_rule([f"Free({nr},{nc})"],f"Safe({nr},{nc})")
                self.kb.add_rule([f"Free({nr},{nc})",f"Safe({nr},{nc})"],f"CanMove({nr},{nc})")

            #when the cell is 1, then it is obstacle
            elif cell == 1:
                # add facts
                self.kb.tell(f"Obstacle({nr},{nc})")
                self.kb.tell(f"NotSafe({nr},{nc})")

                # add rule
                self.kb.add_rule([f"Obstacle({nr},{nc})"], f"NotSafe({nr},{nc})")


    def reason(self):
        """Use logic inference to make decisions."""
        # TODO: Implement

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

    
    def act(self):
        """Decide and execute next action."""
        # TODO: Implement

        #here where the agent decide to which of the neighbor cells to move
        #the logic is as following

        #first we identify the position of agent as row=r, column=c coordinates
        r, c = self.env.agent_pos
        
        #then we identify the neighbors
        neighbors = self.env.get_neighbors((r,c))

        safe_moves = []

        #now for each neighbor we ask kb if it's safe to move to it
        #so we check the fact accross all neighbors (CanMove(nr,nc))
        for nr, nc in neighbors:
            if self.kb.ask(f"CanMove({nr},{nc})"):
                safe_moves.append((nr, nc))

        
         # If we have safe moves, pick the BEST one
        if safe_moves:
            # Prefer the one closer to the goal and avoid going back if possible
            safe_moves_sorted = sorted(
                safe_moves,
                key=lambda cell: (
                    self.env.manhattan_distance(cell, self.env.goal)
                )
            )
            return safe_moves_sorted[0]
        #if no safe neifgbor, the agent stay in its current position
        return (r,c)