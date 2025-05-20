import yaml
from reward_agents.planner import Planner
# from reward_agent.factuality_agent import FactualityAgent
# from reward_agent.constraint_agent import ConstraintAgent

if __name__ == "__main__":
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    agents_cfg = config["agents"]

    # Instantiate agents with their specific configs
    planner = Planner(agents_cfg["planner"])
    # factuality_agent = FactualityAgent(agents_cfg["factuality"])
    # constraint_agent = ConstraintAgent(agents_cfg["constraint"])

    # Example run: Planner
    test_cases = [
        "Write a JSON list with exactly 5 city names.",
        "Summarise the main events of World War II.",
        "Generate a limerick that rhymes with 'Singapore'.",
    ]
    for t in test_cases:
        print(f"▶ {t}\n  → {planner(t) or '[]'}\n")

    # # Example run: Factuality
    # fact_text = "Singapore is the capital of Malaysia."
    # print("Factuality check result:", factuality_agent(fact_text))

    # # Example run: Constraint
    # constraint_text = "List exactly three fruits."
    # print("Constraint check result:", constraint_agent("Apple, Banana, Orange", "List exactly three fruits."))
