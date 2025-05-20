# Agentic Multi-Agent Reward Modeling System

- Modular agents (Planner, Factuality, Constraint, etc.), each with their own LLM and config
- Global config.yaml for all agent settings
- Easy to extend: create new agent by subclassing AgentBase

## Run Example

    pip install -r requirements.txt
    python scripts/run_agents.py
