def bmi_status(bmi: float, weight: float, height: float):
    
    height_m = height / 100

    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)

    min_weight = round(min_weight, 2)
    max_weight = round(max_weight, 2)

    # UNDERWEIGHT
    if bmi < 18.5:

        gain = round(min_weight - weight, 2)

        foods = [
            "Milk",
            "Eggs",
            "Peanut butter",
            "Bananas",
            "Rice",
            "Potatoes",
            "Nuts"
        ]

        diseases = [
            "Weak immune system",
            "Anemia",
            "Bone weakness",
            "Fatigue"
        ]

        cholesterol = "Low cholesterol risk but may have nutritional deficiency."

        return (
            "Underweight",
            f"You should gain about {gain} kg to reach a healthy weight.",
            foods,
            diseases,
            cholesterol
        )

    # NORMAL
    elif 18.5 <= bmi < 25:

        foods = [
            "Vegetables",
            "Fruits",
            "Whole grains",
            "Fish",
            "Lean chicken"
        ]

        diseases = [
            "Low health risk"
        ]

        cholesterol = "Normal cholesterol risk if diet and exercise are maintained."

        return (
            "Normal",
            "Your weight is healthy. Maintain your lifestyle.",
            foods,
            diseases,
            cholesterol
        )

    # OVERWEIGHT
    else:

        reduce = round(weight - max_weight, 2)

        foods = [
            "Oats",
            "Green vegetables",
            "Salads",
            "Fruits",
            "Brown rice",
            "Green tea"
        ]

        diseases = [
            "Heart disease",
            "High blood pressure",
            "Type 2 diabetes",
            "Fatty liver"
        ]

        cholesterol = "High cholesterol risk. Reduce oily and fried foods."

        return (
            "Overweight",
            f"You should reduce about {reduce} kg to reach a healthy weight.",
            foods,
            diseases,
            cholesterol
        )
