def get_diet_plan(goal):
    if goal == "Weight Loss":
        return {
            "breakfast": "Oats + Fruits",
            "lunch": "Grilled chicken + rice",
            "dinner": "Salad + soup"
        }

    if goal == "Muscle Gain":
        return {
            "breakfast": "Eggs + toast",
            "lunch": "Chicken + rice",
            "dinner": "Paneer + roti"
        }

    return {
        "breakfast": "Balanced breakfast",
        "lunch": "Balanced lunch",
        "dinner": "Light dinner"
    }