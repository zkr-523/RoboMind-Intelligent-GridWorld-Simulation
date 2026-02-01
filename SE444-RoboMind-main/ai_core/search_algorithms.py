from typing import Tuple, List, Optional
from collections import deque
import heapq


def bfs(env, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List], float, int]:
    """
    Breadth-First Search - Find shortest path in terms of number of steps.
    """
    
    queue = deque([start]) # create the Frontier 
    visited = {start} # the visited cells to avoid so never visit it twice
    parent = {start: None} #store path
    expanded = 0 #how many nodes you popped and processed
  
    while queue:
        current = queue.popleft() # Remove NEXT node to explore
        expanded += 1 #Count this as an expanded node
        
        if current == goal: 
            path = reconstruct_path(parent,start,goal)   #Build the final path for the search   
            cost = len(path) - 1  # BFS cost is number of steps
            print("the Path is ", path)
            return path, cost, expanded
        
        for neighbor in env.get_neighbors(current):#Explore all valid neighbors
            if neighbor not in visited:# to skip the visited nodes
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor) # add the frontier 
    
    return None, float('inf'), expanded  # No path found 
   


def ucs(env, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List], float, int]:
    """
    Uniform Cost Search - Find path with lowest total cost.
    
    """
    
    frontier = [(0, start)]  # the frontier(cost, position)
    explored = set() #prevents reprocessing nodes
    cost_so_far = {start: 0} # remember the cheapest cost found so far 
    parent = {start: None}
    expanded = 0 #how many nodes you popped and processed
    
    while frontier:
        current_cost, current = heapq.heappop(frontier)# Pops LOWEST COST node → guarantees optimality
        
        
        if current in explored:
            continue #Skip if already fully processed
        
        explored.add(current)
        expanded += 1
        
        if current == goal:
            path = reconstruct_path(parent,start,goal)#Build the final path for the search 
            print("The path is :",path)
            return path, current_cost, expanded # UCS returns actual g(goal)
        
        for neighbor in env.get_neighbors(current):
            new_cost = current_cost + env.get_cost(current, neighbor)
            
            if neighbor not in explored:
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost # update the best cost
                    parent[neighbor] = current # Update path
                    heapq.heappush(frontier, (new_cost, neighbor))
                    
    return None, float('inf'), expanded
    


def astar(env, start: Tuple[int, int], goal: Tuple[int, int], 
          heuristic='manhattan') -> Tuple[Optional[List], float, int]:
    """
    A* Search - Find optimal path using cost + heuristic.
    """
    
    # Choose heuristic function
    # Heuristic h(n): estimated cost from n → goal
    if heuristic == 'manhattan':
        h = lambda pos: env.manhattan_distance(pos, goal)
    elif heuristic == 'euclidean':
        h = lambda pos: env.euclidean_distance(pos, goal)
    else:
        raise ValueError(f"Unknown heuristic: {heuristic}")
    
    # A* uses f(n) = g(n) + h(n) as priority
    g_score = {start: 0}#g(n): cost from start to node
    f_score = {start: h(start)}
    frontier = [(f_score[start], start)]  # (f_score, position) Priority queue sorted by f(n)
    explored = set()#Track expanded nodes
    parent = {start: None} # Store path
    expanded = 0
    
    while frontier:
        current_f, current = heapq.heappop(frontier)# Pop node with SMALLEST f(n) value 
        
        if current in explored:
            continue
        
        explored.add(current)
        expanded += 1
        
        if current == goal:
           path = reconstruct_path(parent,start,goal)#Build the final path for the search 
           print("the Path is ", path)
           return path, g_score[current], expanded
        
        for neighbor in env.get_neighbors(current):
            if neighbor in explored:
                continue
            
            tentative_g = g_score[current] + env.get_cost(current, neighbor)
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g # Update g(n)
                f_score[neighbor] = tentative_g + h(neighbor)  # Compute f(n)
                parent[neighbor] = current
                heapq.heappush(frontier, (f_score[neighbor], neighbor))
    
    return None, float('inf'), expanded
    


def reconstruct_path(parent: dict, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Reconstruct path from parent pointers.
    """
    
    path = []
    node = goal
    while node is not None:
        path.append(node)# Add node to path
        node=parent[node]# Move backwards through parent pointers
    path.reverse()# Reverse to get path from start → goal
    return path


# ============================================================================
# Testing Code (You can run this file directly to test your implementations)
# ============================================================================

if __name__ == "__main__":
    from environment import GridWorld
    
    print("=" * 60)
    print("  Testing Search Algorithms")
    print("=" * 60 + "\n")
    
    # Create a test environment
    env = GridWorld(width=10, height=10)
    
    # Add obstacles
    for i in range(3, 8):
        env.add_obstacle(i, 5)
    
    start = (0, 0)
    goal = (9, 9)
    
    print(f"Grid: {env.width}x{env.height}")
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Test each algorithm
    algorithms = [
        ('BFS', lambda: bfs(env, start, goal)),
        ('UCS', lambda: ucs(env, start, goal)),
        ('A* (Manhattan)', lambda: astar(env, start, goal, 'manhattan')),
        ('A* (Euclidean)', lambda: astar(env, start, goal, 'euclidean')),
    ]
    
    results = []
    
    for name, algo_func in algorithms:
        print(f"\nTesting {name}...")
        print("-" * 40)
        try:
            path, cost, expanded = algo_func()
            if path:
                print(f"✓ Success!")
                print(f"  Path length: {len(path)} steps")
                print(f"  Path cost: {cost:.2f}")
                print(f"  Nodes expanded: {expanded}")
                results.append((name, True, len(path), cost, expanded))
            else:
                print(f"✗ No path found")
                results.append((name, False, 0, 0, 0))
        except NotImplementedError:
            print(f"⚠️  Not implemented yet")
            results.append((name, False, 0, 0, 0))
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append((name, False, 0, 0, 0))
    
    # Summary table
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"{'Algorithm':<20} {'Status':<10} {'Length':<8} {'Cost':<8} {'Expanded':<10}")
    print("-" * 60)
    
    for name, success, length, cost, expanded in results:
        status = "✓" if success else "✗"
        length_str = str(length) if success else "-"
        cost_str = f"{cost:.2f}" if success else "-"
        expanded_str = str(expanded) if success else "-"
        print(f"{name:<20} {status:<10} {length_str:<8} {cost_str:<8} {expanded_str:<10}")
    
    print("-" * 60)
    print("\n💡 Tip: Implement the algorithms one at a time and test each one!")
    print("   Start with BFS (simplest), then UCS, then A*\n")