# 🤖 RoboMind – Intelligent GridWorld Simulation

A Python-based AI simulation where rational agents navigate a 2D grid world using three integrated reasoning techniques: **search algorithms**, **logical inference**, and **Bayesian probabilistic reasoning**.

---

## 🧠 Overview

RoboMind implements a multi-technique AI agent that can intelligently navigate complex grid environments with obstacles and uncertainty. The project demonstrates how different AI paradigms can be combined into a single rational agent capable of planning, reasoning, and adapting to uncertain environments.

Four agent types are implemented and compared:

| Agent | Technique | Description |
|-------|-----------|-------------|
| `SearchAgent` | BFS / UCS / A* | Finds optimal paths using classical search |
| `LogicAgent` | Propositional Logic | Infers safe moves via forward chaining |
| `ProbabilisticAgent` | Bayesian Inference | Handles sensor uncertainty with belief maps |
| `HybridAgent` | All three combined | Integrates search + logic + probability for optimal decisions |

---

## 🏗️ Project Structure

```
RoboMind/
├── main.py                        # Entry point — run simulations
├── environment.py                 # GridWorld simulator
├── requirements.txt
├── agents/
│   ├── search_agent.py            # BFS, UCS, A* navigation
│   ├── logic_agent.py             # Logic-based safe move inference
│   ├── probabilistic_agent.py     # Bayesian belief navigation
│   └── hybrid_agent.py            # Integrated rational agent
├── ai_core/
│   ├── search_algorithms.py       # Core BFS, UCS, A* implementations
│   ├── knowledge_base.py          # Propositional KB with forward chaining
│   └── bayes_reasoning.py         # Bayesian update & belief propagation
└── maps/
    ├── simple.txt                 # Basic test map
    └── maze.txt                   # Complex maze environment
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/zkr-523/RoboMind-Intelligent-GridWorld-Simulation.git
cd RoboMind-Intelligent-GridWorld-Simulation
pip install -r requirements.txt
```

### Running the Simulation

```bash
# Environment demo
python main.py --demo

# Test individual agents
python main.py --test-search
python main.py --test-logic
python main.py --test-probability
python main.py --test-hybrid

# Run all experiments
python main.py --experiment all

# Use a fixed seed for reproducible results
python main.py --test-hybrid --seed 42
```

---

## 🔍 How It Works

### Search Agent
Implements three classical search algorithms in `ai_core/search_algorithms.py`:
- **BFS** – Finds the shortest path by number of steps
- **UCS** – Finds the least-cost path using a priority queue
- **A\*** – Optimal search using Manhattan/Euclidean heuristics for faster convergence

### Logic Agent
Uses a propositional **Knowledge Base** with forward chaining:
- Perceives the environment and asserts facts (`Free`, `Safe`, `Obstacle`, `Goal`)
- Applies rules (e.g., `Free(r,c) ∧ Safe(r,c) → CanMove(r,c)`) to infer safe moves
- Only moves to cells the KB confirms are safe

### Probabilistic Agent
Maintains a **belief map** across the entire grid:
- Each cell holds a probability estimate of containing an obstacle
- Beliefs are updated at every step using Bayes' rule based on sensor readings
- Agent navigates toward lower-belief (safer) cells closest to the goal

### Hybrid Agent
Integrates all three approaches with a priority-based decision strategy:
1. **Logic first** – filters moves to only logically safe cells
2. **Search second** – runs A* from current position among safe candidates
3. **Probability fallback** – uses belief map when logic has no safe options
4. **Exploration bias** – prefers unvisited cells to avoid oscillation

---

## 📊 Performance Metrics

Agents are evaluated on:
- **Path Length** – total steps taken to reach goal
- **Nodes Expanded** – search efficiency
- **Success Rate** – goal reached within step budget
- **Belief Accuracy** – correctness of probabilistic estimates (probabilistic agent)

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Pygame** – grid world visualization
- **NumPy** – numerical computations and grid operations
- **Matplotlib** – performance plotting

---

## 📚 Concepts Demonstrated

- Uninformed vs. informed search (BFS, UCS, A*)
- Propositional logic and forward chaining inference
- Bayesian belief updates under sensor uncertainty
- Rational agent architecture (perceive → reason → act)
- Multi-technique AI integration

---

## 👤 Author

**Zakariya Ba Alawi**  
Software Engineering Student — Alfaisal University  
[LinkedIn](https://linkedin.com/in/zakariya-s-ba-alawi-a17977276) · [GitHub](https://github.com/zkr-523)
