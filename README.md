# AISG Reward Agents

A modular and extensible agent framework for reasoning tasks using Large Language Models (LLMs). Each agent is responsible for a specific reward dimension (e.g. factuality, constraint satisfaction), and runs independently based on its configuration.

## ✨ Features

- **Modular agents**: Includes `Planner`, `FactualityAgent`, `ConstraintAgent`, etc. Each agent runs its own LLM with a dedicated prompt and configuration.
- **Global configuration**: Centralized `config.yaml` for defining all agents, models, prompts, and shared settings.
- **Extensible**: Add a new agent by subclassing `AgentBase` and defining your `run()` logic and reward computation.

## 🗂️ Folder Structure

```
reward_agents/
│
├── config.yaml               # Global configuration file for all agents
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── scripts/
│   └── run_agents.py         # Main script to launch all agents
│
├── reward_agents/            # Core Python module
│   ├── base.py               # AgentBase class – interface for all agents
│   ├── planner.py            # Planning agent for task decomposition
│   ├── factuality.py         # Agent for evaluating factual correctness
│   ├── constraint.py         # Agent for constraint checking
│   ├── ...                   # Add other agents or utilities here
│
└── .git/                     # Git tracking files (can be ignored)
```

## 🚀 Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run all agents as defined in config.yaml
python -m scripts.run_agents
```

> Make sure your environment has access to required model weights (e.g. via Hugging Face).

## 🛠️ Adding a New Agent

To add a new reward agent:

1. Create a new file in `reward_agents/` (e.g. `helpfulness.py`)
2. Subclass `AgentBase` and implement the `run()` method
3. Add your agent to `config.yaml` under the appropriate section
