"""
RoboMind - Main Entry Point
SE444 - Artificial Intelligence Course Project

Run different modes of the simulation:
    python main.py --demo              # Run environment demo
    python main.py --test-search       # Test search algorithms
    python main.py --test-logic        # Test logic agent
    python main.py --test-probability  # Test probabilistic agent
    python main.py --test-hybrid       # Test hybrid agent
    python main.py --experiment all    # Run all experiments
"""

import argparse
import sys
from environment import GridWorld, demo as env_demo

# Import agent modules (students will implement these)
try:
    from agents.search_agent import SearchAgent
except ImportError:
    SearchAgent = None
    
try:
    from agents.logic_agent import LogicAgent
except ImportError:
    LogicAgent = None
    
try:
    from agents.probabilistic_agent import ProbabilisticAgent
except ImportError:
    ProbabilisticAgent = None
    
try:
    from agents.hybrid_agent import HybridAgent
except ImportError:
    HybridAgent = None


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def run_demo():
    """Run environment demonstration."""
    print_header("RoboMind Environment Demo")
    print("This demo shows the grid world environment.")
    print("Use arrow keys to move the agent manually.")
    print("Press 'R' to reset to start position.\n")
    env_demo()


def test_search():
    """Test search algorithms."""
    print_header("Testing Search Algorithms")
    
    if SearchAgent is None:
        print("❌ SearchAgent not implemented yet!")
        print("Please implement agents/search_agent.py")
        return
    
    # Create environment
    env = GridWorld(width=10, height=10, cell_size=50)
    env.add_random_obstacles(15)
    env.start = (0, 0)
    env.goal = (9, 9)
    
    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Create agent
    agent = SearchAgent(env)
    
    # Test each algorithm
    algorithms = ['bfs', 'ucs', 'astar']
    results = {}
    
    for algo in algorithms:
        print(f"Running {algo.upper()}...")
        try:
            path, cost, expanded = agent.search(algo)
            results[algo] = {
                'path_length': len(path),
                'cost': cost,
                'expanded': expanded,
                'success': path is not None
            }
            print(f"  ✓ Path found! Length: {len(path)}, Cost: {cost}, Expanded: {expanded}")
        except NotImplementedError:
            print(f"  ⚠️  {algo.upper()} not implemented yet")
            results[algo] = {'success': False}
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[algo] = {'success': False}
    
    # Summary
    print("\n" + "-" * 60)
    print("SUMMARY:")
    print("-" * 60)
    print(f"{'Algorithm':<12} {'Success':<10} {'Path Length':<12} {'Nodes Expanded':<15}")
    print("-" * 60)
    for algo, result in results.items():
        if result['success']:
            print(f"{algo.upper():<12} {'✓':<10} {result['path_length']:<12} {result['expanded']:<15}")
        else:
            print(f"{algo.upper():<12} {'✗':<10} {'-':<12} {'-':<15}")
    print("-" * 60)


def test_logic(seed: int | None = None):
    """Test logic-based agent."""
    print_header("Testing Logic Agent")
    
    if LogicAgent is None:
        print("LogicAgent not implemented yet!")
        print("Please implement agents/logic_agent.py")
        return
    
    # Seeding for reproducible demos
    import numpy as np
    import random
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        print(f"Seed: {seed}")
    else:
        print("Seed: random")

    # Create environment
    env = GridWorld(width=10, height=10, cell_size=50)

    # Randomize start and goal positions ensuring they differ
    rng = np.random.default_rng(seed if seed is not None else None)
    env.start = (int(rng.integers(0, env.height)), int(rng.integers(0, env.width)))
    env.goal = env.start
    while env.goal == env.start:
        env.goal = (int(rng.integers(0, env.height)), int(rng.integers(0, env.width)))
    env.agent_pos = env.start

    # Add random obstacles with density cap, avoiding start/goal
    total_cells = env.width * env.height
    requested_density = 0.18  # slightly higher than probability test
    max_density_cap = 0.25
    num_obstacles_requested = int(total_cells * requested_density)
    max_obstacles_allowed = int((total_cells - 2) * max_density_cap)
    num_obstacles = min(num_obstacles_requested, max_obstacles_allowed)
    env.add_random_obstacles(num_obstacles)

    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")

    # Initialize display
    env.init_display()

    # Create logic agent
    agent = LogicAgent(env)

    max_steps = env.width * env.height
    steps = 0
    reached = False

    while env.running and steps < max_steps:
        # Handle window events
        if not env.handle_events():
            break

        # If at goal, stop
        if env.is_goal(env.agent_pos):
            reached = True
            env.render()
            break

        # Agent cycle: perceive → reason → act
        agent.perceive()
        agent.reason()
        next_pos = agent.act()

        # Move if different
        if next_pos != env.agent_pos:
            env.visited.add(env.agent_pos)
            env.path.append(next_pos)
            env.agent_pos = next_pos
            env.expanded += 1

        # Render and small delay
        env.render()
        try:
            import pygame
            pygame.time.delay(300)  # slower animation
        except Exception:
            import time
            time.sleep(0.3)

        steps += 1

    env.close()
    if reached:
        print(" Goal reached!")
        print(f"Path Length: {len(env.path)} | Expanded: {env.expanded}")
    else:
        print(" Goal not reached.")
        print(f"Path Length: {len(env.path)} | Expanded: {env.expanded}")


def test_probability(seed: int | None = None):
    """Test probabilistic agent."""
    print_header("Testing Probabilistic Agent")
    
    
    
    # Seeding for reproducible demos
    import numpy as np
    import random
    if seed is not None:
        # Use provided seed for reproducibility
        np.random.seed(seed)
        random.seed(seed)
        print(f"Seed: {seed}")
    else:
        # Fully random run; do not set global seeds
        print("Seed: random")

    # Create environment with random obstacles and random start/goal
    env = GridWorld(width=10, height=10, cell_size=50)

    # Randomize start and goal positions ensuring they are different and not obstacles
    rng = np.random.default_rng(seed if seed is not None else None)
    env.start = (int(rng.integers(0, env.height)), int(rng.integers(0, env.width)))
    env.goal = env.start
    while env.goal == env.start:
        env.goal = (int(rng.integers(0, env.height)), int(rng.integers(0, env.width)))
    env.agent_pos = env.start

    # Add random obstacles (avoid start/goal) with a hard cap on density
    total_cells = env.width * env.height
    requested_density = 0.15  # requested obstacle density (more open)
    max_density_cap = 0.25    # do not exceed 25% obstacles overall
    num_obstacles_requested = int(total_cells * requested_density)
    max_obstacles_allowed = int((total_cells - 2) * max_density_cap)  # reserve start & goal
    num_obstacles = min(num_obstacles_requested, max_obstacles_allowed)
    env.add_random_obstacles(num_obstacles)

    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")

    # Initialize display
    env.init_display()

    # Create probabilistic agent
    agent = ProbabilisticAgent(env)

    # Simple loop: update beliefs and move toward lowest-risk neighbor
    max_steps = env.width * env.height * 2
    steps = 0
    reached = False
    while env.running and steps < max_steps:
        # Handle window events and render
        if not env.handle_events():
            break

        # If at goal, stop
        if env.is_goal(env.agent_pos):
            reached = True
            env.render()
            break

        # Simulate a sensor reading at current position: it's free if we can stand there
        # Sensor reading: True means obstacle detected at this cell; False means free
        sensor_reading = (env.grid[env.agent_pos[0]][env.agent_pos[1]] == 1)
        agent.update_beliefs(sensor_reading, env.agent_pos)

        # Decide next move
        next_pos = agent.act()
        if next_pos == env.agent_pos:
            # No progress possible; end
            env.render()
            break

        # Update environment state
        env.visited.add(env.agent_pos)
        env.path.append(next_pos)
        env.agent_pos = next_pos
        env.expanded += 1

        # Render frame and slow down step progression
        env.render()
        try:
            import pygame
            pygame.time.delay(300)  # slower animation
        except Exception:
            # Fallback if pygame timing isn't available
            import time
            time.sleep(0.3)
        steps += 1

    env.close()
    if reached:
        print("✓ Goal reached!")
        print(f"Path Length: {len(env.path)} | Expanded: {env.expanded}")
    else:
        print("✗ Goal not reached.")
        print(f"Path Length: {len(env.path)} | Expanded: {env.expanded}")


def test_hybrid(seed: int | None = None):
    """Test hybrid agent with search + logic + probability."""
    print_header("Testing Hybrid Agent")
    

    # Seeding for reproducibility
    import numpy as np
    import random
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        print(f"Seed: {seed}")
    else:
        print("Seed: random")

    # Create environment
    env = GridWorld(width=10, height=10, cell_size=50)

    # Randomize start and goal positions ensuring they differ
    rng = np.random.default_rng(seed if seed is not None else None)
    env.start = (int(rng.integers(0, env.height)), int(rng.integers(0, env.width)))
    env.goal = env.start
    while env.goal == env.start:
        env.goal = (int(rng.integers(0, env.height)), int(rng.integers(0, env.width)))
    env.agent_pos = env.start

    # Add random obstacles with density cap
    total_cells = env.width * env.height
    requested_density = 0.18
    max_density_cap = 0.25
    num_obstacles_requested = int(total_cells * requested_density)
    max_obstacles_allowed = int((total_cells - 2) * max_density_cap)
    num_obstacles = min(num_obstacles_requested, max_obstacles_allowed)
    env.add_random_obstacles(num_obstacles)

    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")

    # Initialize display
    env.init_display()

    # Create hybrid agent
    agent = HybridAgent(env)

    max_steps = env.width * env.height * 2
    steps = 0
    reached = False

    while env.running and steps < max_steps:
        # Handle window events
        if not env.handle_events():
            break

        # If at goal, stop
        if env.is_goal(env.agent_pos):
            reached = True
            env.render()
            break

        # Agent cycle: perceive → reason → act (belief updates inside perceive/act)
        agent.perceive()
        agent.reason()
        next_pos = agent.act()

        # If no movement possible after multiple attempts, stop
        if next_pos is None:
            env.render()
            break
        
        # Allow same position occasionally (e.g., replanning), but track it
        if next_pos == env.agent_pos:
            # Don't break immediately - let agent try again
            steps += 1
            continue

        # Apply movement
        env.visited.add(env.agent_pos)
        env.path.append(next_pos)
        env.agent_pos = next_pos
        env.expanded += 1

        # Render and delay
        env.render()
        try:
            import pygame
            pygame.time.delay(200)
        except Exception:
            import time
            time.sleep(0.3)

        steps += 1

    env.close()
    if reached:
        print("✓ Goal reached!")
        print(f"Path Length: {len(env.path)} | Expanded: {env.expanded}")
    else:
        print("✗ Goal not reached.")
        print(f"Path Length: {len(env.path)} | Expanded: {env.expanded}")


def run_experiments():
    """Run comprehensive experiments."""
    test_search()
    test_probability()
    test_logic()
    test_hybrid()
    

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RoboMind - SE444 AI Course Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo              # Run environment demo
  python main.py --test-search       # Test search algorithms  
  python main.py --test-logic        # Test logic agent
  python main.py --test-probability  # Test probabilistic agent
  python main.py --test-hybrid       # Test hybrid agent
  python main.py --experiment all    # Run all experiments
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run environment demonstration')
    parser.add_argument('--test-search', action='store_true',
                       help='Test search algorithms')
    parser.add_argument('--test-logic', action='store_true',
                       help='Test logic-based agent')
    parser.add_argument('--test-probability', action='store_true',
                       help='Test probabilistic agent')
    parser.add_argument('--seed', type=int,
                       help='Set random seed for reproducible demo/tests')
    parser.add_argument('--test-hybrid', action='store_true',
                       help='Test hybrid agent')
    parser.add_argument('--experiment', choices=['all', 'search', 'logic', 'probability'],
                       help='Run experiments')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        print_header("Welcome to RoboMind!")
        print("SE444 - Artificial Intelligence Course Project\n")
        print("To get started, run:")
        print("  python main.py --demo\n")
        print("For all options:")
        print("  python main.py --help\n")
        return
    
    # Run requested mode
    if args.demo:
        run_demo()
    elif args.test_search:
        test_search()
    elif args.test_logic:
        test_logic(args.seed)
    elif args.test_probability:
        test_probability(args.seed)
    elif args.test_hybrid:
        test_hybrid(args.seed)
    elif args.experiment:
        run_experiments()


if __name__ == "__main__":
    main()