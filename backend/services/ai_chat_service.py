def ai_reply(question):
    q = question.lower()

    if "protein" in q:
        return "You should consume 1.6–2g protein per kg body weight daily."

    if "weight loss" in q:
        return "Focus on calorie deficit, daily walking, and high protein intake."

    if "muscle" in q or "gain" in q:
        return "Train with progressive overload and eat sufficient calories."

    if "workout" in q:
        return "Workout at least 4–5 days per week with rest days."

    if "water" in q:
        return "Drink at least 3 liters of water daily."

    return "Stay consistent! Small daily habits lead to big results 💪"