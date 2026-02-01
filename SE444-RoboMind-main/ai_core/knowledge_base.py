"""
Knowledge Base - Logic Reasoning Module
SE444 - Artificial Intelligence Course Project

TODO: Implement propositional logic knowledge base with inference
Phase 2 (Week 3-4)
"""

from typing import Set, List


class KnowledgeBase:
    """
    A simple knowledge base for propositional logic.
    
    Stores facts and rules, performs forward chaining inference.
    """
    
    def __init__(self):
        """Initialize empty knowledge base."""
        self.facts = set()   # Known facts: "Safe(2,3)", "Obstacle(4,5)"
        self.rules = []      # Rules: ("A", "B", "C") means "A AND B → C"
    
    def tell(self, fact: str):
        """
        Add a fact to the knowledge base.
        
        Args:
            fact: A proposition like "Safe(2,3)" or "Explored(5,6)"
        
        Example:
            >>> kb = KnowledgeBase()
            >>> kb.tell("Safe(2,3)")
            >>> kb.tell("Free(2,3)")
        """
        # TODO: Implement
        self.facts.add(fact)
        print(f"Added fact: {fact}")
    
    def add_rule(self, premises: List[str], conclusion: str):
        """
        Add an inference rule.
        
        Args:
            premises: List of propositions that must all be true
            conclusion: Proposition that follows from premises
        
        Example:
            >>> kb.add_rule(["Safe(X)", "Free(X)"], "CanMove(X)")
            This means: If Safe(X) AND Free(X) then CanMove(X)
        """
        # TODO: Implement
        self.rules.append((premises, conclusion))
        print(f"Added rule: {' AND '.join(premises)} → {conclusion}")
    
    def ask(self, query: str) -> bool:
        """
        Check if a query can be inferred from the knowledge base.
        
        Args:
            query: A proposition to check
        
        Returns:
            True if query is known or can be inferred, False otherwise
        
        Example:
            >>> kb.ask("Safe(2,3)")
            True
        """
        # TODO: Implement proper inference
        # For now, just check if it's in facts
        #first we check if the query in facts
        if query in self.facts:
            #if so return true that the query is in facts
            return True
        #else inference using infer()
        #to check if new facts can be drived
        self.infer()
        #after infer then return True (if the query drived) or False (otherwise)
        return query in self.facts
    
    def infer(self):
        """
        Apply forward chaining to derive new facts from rules.
        
        Forward chaining:
            1. For each rule: check if all premises are satisfied
            2. If yes, add conclusion to facts
            3. Repeat until no new facts can be derived
        
        Example:
            >>> kb.tell("Safe(2,3)")
            >>> kb.tell("Free(2,3)")
            >>> kb.add_rule(["Safe(2,3)", "Free(2,3)"], "CanMove(2,3)")
            >>> kb.infer()
            >>> kb.ask("CanMove(2,3)")
            True
        """
        # TODO: Implement forward chaining
        #loop that keep running while new facts are being added to the KB
        #and the loop is controlled with a flag that check if new facts were added
        #the infer process will stop whenever fact_added become false (as no fact added to KB)
        fact_added = True
        while fact_added:
            #initally assume no fact will be added
            #this will stop the loop if no new fact added to KB
            fact_added = False
            #itertae through all rules (premises list, conclusion)
            #and check if premises exists in facts
            for premises, conclusion in self.rules:
                if all(p in self.facts for p in premises):
                    #if the premises satisfied the facts, check if the conclusion is new
                    #to add it to the facts and set flag (fact_added = True)
                    if conclusion not in self.facts:
                        self.facts.add(conclusion)
                        fact_added = True
                       
        # raise NotImplementedError("Forward chaining not implemented yet!")
    
    def __str__(self) -> str:
        """String representation of KB."""
        return f"KB with {len(self.facts)} facts and {len(self.rules)} rules"


# ============================================================================
# Testing Code
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Knowledge Base")
    print("=" * 60 + "\n")
    
    # Create KB
    kb = KnowledgeBase()
    
    # Add some facts
    print("Adding facts...")
    kb.tell("Safe(2,3)")
    kb.tell("Free(2,3)")
    kb.tell("Adjacent(2,3,2,4)")
    
    # Add some rules
    print("\nAdding rules...")
    kb.add_rule(["Safe(2,3)", "Free(2,3)"], "CanMove(2,3)")
    kb.add_rule(["Safe(2,3)", "Adjacent(2,3,2,4)", "Free(2,4)"], "SafePath(2,3,2,4)")
    
    # Query
    print("\nQuerying...")
    print(f"Is Safe(2,3) known? {kb.ask('Safe(2,3)')}")
    print(f"Is Obstacle(2,3) known? {kb.ask('Obstacle(2,3)')}")
    print(f"Is canMove(2,3) known? {kb.ask('CanMove(2,3)')}")
    
    # Try inference
    print("\nTrying inference...")
    try:
        kb.infer()
        print(f"After inference, is CanMove(2,3) known? {kb.ask('CanMove(2,3)')}")
    except NotImplementedError:
        print("⚠️  Forward chaining not implemented yet!")
    
    print(f"\n{kb}")
    print("\n💡 Tip: Implement forward chaining to automatically derive new facts!")