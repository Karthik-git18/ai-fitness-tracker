import pandas as pd
from flask import Flask, send_from_directory, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ---------- LOAD DATASET ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "datasets", "nutrition.csv")

nutrition_df = pd.read_csv(DATA_PATH)

# ✅ CLEAN COLUMN NAMES
nutrition_df.columns = nutrition_df.columns.str.strip().str.lower()

# ✅ CLEAN FOOD NAMES
nutrition_df["food"] = nutrition_df["food"].astype(str).str.lower().str.strip()

# ✅ KEEP ONLY VALID ROWS
nutrition_df = nutrition_df.dropna(subset=["food", "calories", "protein"])
nutrition_df["calories"] = pd.to_numeric(nutrition_df["calories"], errors="coerce")
nutrition_df["protein"] = pd.to_numeric(nutrition_df["protein"], errors="coerce")
nutrition_df = nutrition_df.dropna()

print("Loaded columns:", nutrition_df.columns)
print("Total foods:", len(nutrition_df))

L = {"sets": 4, "reps": "8–12", "rest": "60–90 sec"}

# ---------- ROOT ----------
@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(FRONTEND_DIR, path)
# ---------- HOME ----------
@app.route("/home", methods=["POST"])
def home():
    u = request.json

    weight = u["weight"]
    height = u["height"]
    age = u["age"]
    gender = u.get("gender", "Male")
    goal = u["goal"]

    # ---- BMR ----
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # ---- Goal adjustment ----
    if goal == "Weight Loss":
        calories = int(bmr * 1.2 - 400)
        protein = int(weight * 1.8)
    elif goal == "Muscle Gain":
        calories = int(bmr * 1.5 + 300)
        protein = int(weight * 2.2)
    else:
        calories = int(bmr * 1.4)
        protein = int(weight * 1.6)

    water = round(weight * 0.033, 1)
    bmi = round(weight / ((height / 100) ** 2), 2)

    weekly_workout = [
        {"day": "Monday", "focus": "Chest + Triceps"},
        {"day": "Tuesday", "focus": "Back + Biceps"},
        {"day": "Wednesday", "focus": "Legs"},
        {"day": "Thursday", "focus": "Shoulders"},
        {"day": "Friday", "focus": "Core + Cardio"},
        {"day": "Saturday", "focus": "Full Body"},
        {"day": "Sunday", "focus": "Rest"}
    ]

    return jsonify({
        "calories": calories,
        "protein": protein,
        "water": water,
        "bmi": bmi,
        "weekly_workout": weekly_workout
    })

# ---------------- CALC TARGETS ----------------
def calculate_targets(user):
    weight = user["weight"]
    height = user["height"]
    age = user["age"]
    goal = user["goal"]

    # Mifflin-St Jeor (male default)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    maintenance = bmr * 1.55

    if goal == "Weight Loss":
        calories = maintenance - 500
        protein = weight * 1.8
    elif goal == "Muscle Gain":
        calories = maintenance + 400
        protein = weight * 2.2
    else:
        calories = maintenance
        protein = weight * 1.6

    return int(calories), int(protein)

# ---------------- PICK FOODS ----------------
def pick_foods(target_cal, target_protein):
    foods = nutrition_df.sample(200)

    selected = []
    total_cal = 0
    total_pro = 0

    for _, row in foods.iterrows():
        if total_cal < target_cal and total_pro < target_protein:
            selected.append({
                "food": row["food"],
                "calories": int(row["calories"]),
                "protein": int(row["protein"]),
            })
            total_cal += row["calories"]
            total_pro += row["protein"]

        if total_cal >= target_cal and total_pro >= target_protein:
            break

    return selected
# ---------------- DIET API ----------------
@app.route("/diet", methods=["POST"])
def diet():
    user = request.json

    daily_cal, daily_pro = calculate_targets(user)

    plan = {
        "target_calories": daily_cal,
        "target_protein": daily_pro,

        "breakfast": pick_foods(daily_cal * 0.3, daily_pro * 0.3),
        "lunch": pick_foods(daily_cal * 0.4, daily_pro * 0.4),
        "dinner": pick_foods(daily_cal * 0.3, daily_pro * 0.3),
    }

    return jsonify(plan)
# ---------- FOOD SCAN ----------
@app.route("/scan-food", methods=["POST"])
def scan_food():
    data = request.json
    food = data.get("food", "").lower().strip()

    if not food:
        return jsonify({"error": "Food name missing"}), 400

    # ✅ MATCH FOOD SAFELY
    match = nutrition_df[
        nutrition_df["food"].str.contains(food, na=False)
    ]

    if match.empty:
        return jsonify({
            "food": food.title(),
            "calories": 0,
            "protein": 0,
            "message": "Food not found in nutrition dataset"
        })

    row = match.iloc[0]

    return jsonify({
        "food": row["food"].title(),
        "calories": int(row["calories"]),
        "protein": float(row["protein"]),
        "category": row.get("category", "General")
    })
# ---------- WORKOUT ----------
@app.route("/workout", methods=["POST"])
def workout():
    goal = request.json.get("goal", "").lower().replace(" ", "_")

    plans = {
        "weight_loss": [
            {
                "day": "Monday",
                "focus": "Upper Body Cardio",
                "exercises": [
                    {"name": "Push Ups", "equipment": "Bodyweight", "sets": 3, "reps": "12–15", "rest": "45 sec"},
                    {"name": "Jumping Jacks", "equipment": "Bodyweight", "sets": 3, "reps": "30 sec", "rest": "30 sec"},
                    {"name": "Rows", "equipment": "Dumbbell", "sets": 3, "reps": "12–15", "rest": "45 sec"},
                ],
            },
            {
                "day": "Tuesday",
                "focus": "Lower Body Cardio",
                "exercises": [
                    {"name": "Burpees", "equipment": "Bodyweight", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                    {"name": "Lunges", "equipment": "Bodyweight", "sets": 3, "reps": "15–20", "rest": "45 sec"},
                    {"name": "High Knees", "equipment": "Bodyweight", "sets": 3, "reps": "30 sec", "rest": "30 sec"},
                ],
            },
            {
                "day": "Wednesday",
                "focus": "Full Body",
                "exercises": [
                    {"name": "Plank", "equipment": "Bodyweight", "sets": 3, "reps": "45 sec", "rest": "30 sec"},
                    {"name": "Mountain Climbers", "equipment": "Bodyweight", "sets": 3, "reps": "30 sec", "rest": "30 sec"},
                    {"name": "Squats", "equipment": "Bodyweight", "sets": 3, "reps": "15–20", "rest": "45 sec"},
                ],
            },
            {
                "day": "Thursday",
                "focus": "Cardio & Core",
                "exercises": [
                    {"name": "Jump Rope", "equipment": "Rope", "sets": 3, "reps": "1 min", "rest": "30 sec"},
                    {"name": "Crunches", "equipment": "Bodyweight", "sets": 3, "reps": "20–25", "rest": "30 sec"},
                    {"name": "Walking", "equipment": "Bodyweight", "sets": 1, "reps": "30 min", "rest": "-"},
                ],
            },
            {
                "day": "Friday",
                "focus": "HIIT",
                "exercises": [
                    {"name": "Sprint", "equipment": "Bodyweight", "sets": 5, "reps": "20 sec", "rest": "40 sec"},
                    {"name": "Rest", "equipment": "Bodyweight", "sets": 1, "reps": "5 min", "rest": "-"},
                ],
            },
            {
                "day": "Saturday",
                "focus": "Light Activity",
                "exercises": [
                    {"name": "Yoga", "equipment": "Mat", "sets": 1, "reps": "30 min", "rest": "-"},
                ],
            },
            {
                "day": "Sunday",
                "focus": "Rest",
                "exercises": [
                    {"name": "Stretching", "equipment": "Bodyweight", "sets": "-", "reps": "15 min", "rest": "-"},
                ],
            },
        ],
        "maintain": [
            {
                "day": "Monday",
                "focus": "Upper Body",
                "exercises": [
                    {"name": "Push Ups", "equipment": "Bodyweight", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                    {"name": "Dumbbell Press", "equipment": "Dumbbell", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                    {"name": "Rows", "equipment": "Dumbbell", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                ],
            },
            {
                "day": "Tuesday",
                "focus": "Lower Body",
                "exercises": [
                    {"name": "Squats", "equipment": "Bodyweight", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                    {"name": "Leg Press", "equipment": "Machine", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                    {"name": "Calf Raises", "equipment": "Bodyweight", "sets": 3, "reps": "12–15", "rest": "45 sec"},
                ],
            },
            {
                "day": "Wednesday",
                "focus": "Cardio",
                "exercises": [
                    {"name": "Running", "equipment": "Bodyweight", "sets": 1, "reps": "20–30 min", "rest": "-"},
                    {"name": "Stretching", "equipment": "Mat", "sets": 1, "reps": "10 min", "rest": "-"},
                ],
            },
            {
                "day": "Thursday",
                "focus": "Full Body",
                "exercises": [
                    {"name": "Burpees", "equipment": "Bodyweight", "sets": 3, "reps": "8–10", "rest": "60 sec"},
                    {"name": "Plank", "equipment": "Bodyweight", "sets": 3, "reps": "45 sec", "rest": "30 sec"},
                    {"name": "Lunges", "equipment": "Bodyweight", "sets": 3, "reps": "10–12", "rest": "60 sec"},
                ],
            },
            {
                "day": "Friday",
                "focus": "Core",
                "exercises": [
                    {"name": "Plank", "equipment": "Bodyweight", "sets": 3, "reps": "60 sec", "rest": "30 sec"},
                    {"name": "Crunches", "equipment": "Bodyweight", "sets": 3, "reps": "20–25", "rest": "30 sec"},
                ],
            },
            {
                "day": "Saturday",
                "focus": "Active Recovery",
                "exercises": [
                    {"name": "Walking", "equipment": "Bodyweight", "sets": 1, "reps": "30 min", "rest": "-"},
                ],
            },
            {
                "day": "Sunday",
                "focus": "Rest",
                "exercises": [
                    {"name": "Meditation", "equipment": "Mat", "sets": "-", "reps": "15 min", "rest": "-"},
                ],
            },
        ],
        "muscle_gain": [
            {
                "day": "Monday",
                "focus": "Chest + Triceps",
                "exercises": [
                    {"name": "Bench Press", "equipment": "Barbell", "variations": ["Incline Bench", "Dumbbell Press"], **L},
                    {"name": "Chest Fly", "equipment": "Dumbbell", "variations": ["Cable Fly", "Pec Deck"], **L},
                    {"name": "Triceps Dips", "equipment": "Bodyweight", "variations": ["Bench Dips", "Weighted Dips"], **L},
                ],
            },
            {
                "day": "Tuesday",
                "focus": "Back + Biceps",
                "exercises": [
                    {"name": "Pull Ups", "equipment": "Bodyweight", "variations": ["Assisted", "Lat Pulldown"], **L},
                    {"name": "Barbell Row", "equipment": "Barbell", "variations": ["Dumbbell Row"], **L},
                    {"name": "Bicep Curl", "equipment": "Dumbbell", "variations": ["Hammer Curl", "Preacher Curl"], **L},
                ],
            },
            {
                "day": "Wednesday",
                "focus": "Legs",
                "exercises": [
                    {"name": "Squats", "equipment": "Barbell", "variations": ["Front Squat", "Goblet Squat"], **L},
                    {"name": "Leg Press", "equipment": "Machine", "variations": ["Hack Squat"], **L},
                    {"name": "Calf Raises", "equipment": "Bodyweight", "variations": ["Seated Calf Raise"], **L},
                ],
            },
            {
                "day": "Thursday",
                "focus": "Shoulders",
                "exercises": [
                    {"name": "Shoulder Press", "equipment": "Dumbbell", "variations": ["Arnold Press"], **L},
                    {"name": "Lateral Raise", "equipment": "Dumbbell", "variations": ["Cable Raise"], **L},
                    {"name": "Rear Delt Fly", "equipment": "Dumbbell", "variations": ["Face Pull"], **L},
                ],
            },
            {
                "day": "Friday",
                "focus": "Arms",
                "exercises": [
                    {"name": "EZ Bar Curl", "equipment": "EZ Bar", "variations": ["Dumbbell Curl"], **L},
                    {"name": "Tricep Pushdown", "equipment": "Cable", "variations": ["Overhead Extension"], **L},
                ],
            },
            {
                "day": "Saturday",
                "focus": "Core",
                "exercises": [
                    {"name": "Plank", "equipment": "Bodyweight", "sets": 3, "reps": "45 sec", "rest": "30 sec"},
                    {"name": "Hanging Leg Raise", "equipment": "Bodyweight", "variations": ["Lying Leg Raise"], **L},
                ],
            },
            {
                "day": "Sunday",
                "focus": "Rest",
                "exercises": [
                    {"name": "Stretching", "equipment": "Bodyweight", "sets": "-", "reps": "15 min", "rest": "-"},
                ],
            },
        ],
    }

    return plans.get(goal, plans["muscle_gain"])

# ---------- SUPPLEMENTS ----------
@app.route("/supplements", methods=["POST"])
def supplements():
    goal = request.json.get("goal", "").lower().replace(" ", "_")

    data = {
        "muscle_gain": [
            {
                "name": "Whey Protein",
                "reason": "Supports muscle recovery and lean muscle growth",
                "dosage": "1 scoop (25–30g protein)",
                "timing": "Post-workout",
                "warning": "Avoid if lactose intolerant",
                "link": "https://hyugalife.com/search?q=whey+protein"
            },
            {
                "name": "Creatine Monohydrate",
                "reason": "Improves strength, power, and workout performance",
                "dosage": "3–5g daily",
                "timing": "Pre or Post workout",
                "warning": "Drink plenty of water",
                "link": "https://hyugalife.com/search?q=creatine"
            },
            {
                "name": "BCAA",
                "reason": "Reduces muscle soreness and fatigue",
                "dosage": "5–10g",
                "timing": "During or Post workout",
                "warning": "Not needed if protein intake is sufficient",
                "link": "https://hyugalife.com/search?q=bcaa"
            }
        ],
        "weight_loss": [
            {
                "name": "Whey Protein (Low Carb)",
                "reason": "Preserves muscle mass while losing fat",
                "dosage": "1 scoop",
                "timing": "Morning or Post workout",
                "warning": "Choose low sugar variant",
                "link": "https://hyugalife.com/search?q=whey+protein"
            },
            {
                "name": "Green Tea Extract",
                "reason": "Boosts metabolism and fat oxidation",
                "dosage": "1 capsule",
                "timing": "Morning",
                "warning": "Avoid at night (contains caffeine)",
                "link": "https://hyugalife.com/search?q=green+tea"
            },
            {
                "name": "Multivitamin",
                "reason": "Prevents micronutrient deficiency",
                "dosage": "1 tablet daily",
                "timing": "After breakfast",
                "warning": "Do not exceed dosage",
                "link": "https://hyugalife.com/search?q=multivitamin"
            }
        ],
        "maintain": [
            {
                "name": "Multivitamin",
                "reason": "Supports overall health and wellness",
                "dosage": "1 tablet daily",
                "timing": "Morning with breakfast",
                "warning": "Check expiry date",
                "link": "https://hyugalife.com/search?q=multivitamin"
            },
            {
                "name": "Omega-3 Fish Oil",
                "reason": "Improves heart and joint health",
                "dosage": "1–2 capsules",
                "timing": "With meals",
                "warning": "May cause fish aftertaste",
                "link": "https://hyugalife.com/search?q=fish+oil"
            },
            {
                "name": "Vitamin D3",
                "reason": "Supports bone health and immunity",
                "dosage": "1000–2000 IU",
                "timing": "Morning",
                "warning": "Don't exceed 4000 IU daily",
                "link": "https://hyugalife.com/search?q=vitamin+d3"
            }
        ],
        "weight_gain": [
            {
                "name": "Mass Gainer",
                "reason": "Provides surplus calories for healthy weight gain",
                "dosage": "2 scoops",
                "timing": "Post workout",
                "warning": "Avoid if diabetic",
                "link": "https://hyugalife.com/search?q=mass+gainer"
            },
            {
                "name": "Whey Protein",
                "reason": "Supports muscle mass",
                "dosage": "1 scoop",
                "timing": "Post workout",
                "warning": "Check ingredient quality",
                "link": "https://hyugalife.com/search?q=whey+protein"
            },
            {
                "name": "Peanut Butter",
                "reason": "Healthy fats & calorie dense",
                "dosage": "2 tbsp",
                "timing": "Anytime",
                "warning": "Avoid if allergic",
                "link": "https://hyugalife.com/search?q=peanut+butter"
            }
        ]
    }

    return data.get(goal, [])

# ---------- TIPS ----------
@app.route("/tips")
def tips():
    return jsonify([
        "Stay consistent",
        "Drink enough water",
        "Sleep well"
    ])

# ---------- AI CHAT ----------
@app.route("/ai/chat", methods=["POST"])
def ai_chat():
    data = request.json
    q = data.get("question", "").lower()
    user = data.get("user", {})

    name = user.get("name", "User")
    goal = user.get("goal", "")
    weight = user.get("weight", 0)
    height = user.get("height", 0)

    bmi = round(weight / ((height / 100) ** 2), 1) if height else 0

    # ---------------- RULES ----------------
    if "calorie" in q or "calories" in q:
        reply = f"{name}, your daily calorie target depends on your goal. For {goal}, stay consistent with your plan."

    elif "protein" in q:
        reply = "Protein helps muscle recovery. Aim for 1.6–2g protein per kg body weight."

    elif "weight loss" in q:
        reply = "For weight loss: calorie deficit, high protein, daily walking, and consistency."

    elif "muscle" in q or "gain" in q:
        reply = "For muscle gain: progressive overload, enough calories, and good sleep."

    elif "bmi" in q:
        reply = f"Your BMI is {bmi}. Maintain balance between diet and exercise."

    elif "workout" in q:
        reply = "A balanced workout includes strength training 4–5 days/week and cardio."

    elif "water" in q:
        reply = "Drink at least 3–4 liters of water daily, more if you exercise."

    elif "hello" in q or "hi" in q:
        reply = f"Hi {name}! 👋 How can I help you today?"

    else:
        reply = "I can help with calories, protein, workouts, diet, BMI, and motivation."

    return jsonify({"reply": reply})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)