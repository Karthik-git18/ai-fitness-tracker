def get_workout_plan(goal):
    return [
        {
            "day": "Monday",
            "focus": "Chest",
            "exercises": [
                {"name": "Push-ups", "sets": 3, "reps": 15},
                {"name": "Bench Press", "sets": 4, "reps": 10}
            ]
        },
        {
            "day": "Wednesday",
            "focus": "Back",
            "exercises": [
                {"name": "Pull-ups", "sets": 3, "reps": 8},
                {"name": "Deadlift", "sets": 3, "reps": 8}
            ]
        }
    ]