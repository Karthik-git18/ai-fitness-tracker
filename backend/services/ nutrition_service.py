import pandas as pd
from config import NUTRITION_CSV

df = pd.read_csv(NUTRITION_CSV)

def get_nutrition(food):
    food = food.lower()
    row = df[df["Food"].str.lower() == food]

    if row.empty:
        return None

    r = row.iloc[0]
    return {
        "food": food,
        "calories": float(r["Calories"]),
        "protein": float(r["Protein"]),
        "carbs": float(r["Carbohydrates"]),
        "fat": float(r["Fat"])
    }