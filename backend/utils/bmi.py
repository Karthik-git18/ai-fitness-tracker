def calculate_bmi(weight, height_cm):
    h = height_cm / 100
    return round(weight / (h * h), 2)