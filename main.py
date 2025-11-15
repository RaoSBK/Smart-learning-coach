from memory.memory_bank import MemoryBank
from agents.planner_agent import PlannerAgent

def main():
    memory = MemoryBank()
    planner = PlannerAgent(memory)

    # Test run
    subjects = ["Digital Electronics", "C Programming", "Maths"]
    plan = planner.run(subjects, "2025-12-01", 3)

    print("Generated Study Plan:")
    for day in plan["schedule"]:
        print(day)

if __name__ == "__main__":
    main()
