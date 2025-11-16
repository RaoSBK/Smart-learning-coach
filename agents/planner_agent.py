class PlannerAgent:
    def __init__(self, memory):
        self.memory = memory

    def create_plan(self, subjects, exam_date, hours):
        plan = []

        for i, sub in enumerate(subjects):
            plan.append({
                "day": f"Day {i+1}",
                "subject": sub,
                "hours": hours
            })

        self.memory.set("study_plan", plan)
        return plan
