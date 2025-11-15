class PlannerAgent:
    def __init__(self, memory):
        self.memory = memory

    def run(self, subjects, exam_date, hours_per_day):
        plan = {
            "subjects": subjects,
            "exam_date": exam_date,
            "hours_per_day": hours_per_day,
            "schedule": []
        }

        # Simple example logic
        for i, subject in enumerate(subjects):
            plan["schedule"].append({
                "day": f"Day {i+1}",
                "task": f"Study {subject} for {hours_per_day} hours"
            })

        # Save to memory
        self.memory.set("latest_study_plan", plan)
        return plan
