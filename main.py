import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight_enc TEXT NOT NULL,
    height_enc TEXT NOT NULL,
    bmi REAL NOT NULL,
    status TEXT NOT NULL,
    advice TEXT NOT NULL
)
""")
conn.commit()

# ---------------- ENCRYPTION ----------------
FERNET_KEY = b'O-kN4m4NGeO9nz9JlZBCnsnPMandHr246jkURuRXVLA='
fernet = Fernet(FERNET_KEY)

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

# ---------------- INPUT MODEL ----------------
class BMIInput(BaseModel):
    weight: float
    height: float

# ---------------- BMI STATUS FUNCTION ----------------
def bmi_status(bmi: float, weight: float, height: float):

    height_m = height / 100

    min_weight = round(18.5 * (height_m ** 2), 2)
    max_weight = round(24.9 * (height_m ** 2), 2)

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
            "Nuts & dry fruits"
        ]

        return (
            "Underweight",
            f"You need to gain about {gain} kg to reach a healthy weight.",
            foods
        )

    # NORMAL
    elif 18.5 <= bmi < 25:

        foods = [
            "Vegetables",
            "Fruits",
            "Whole grains",
            "Lean chicken",
            "Fish",
            "Nuts",
            "Healthy home food"
        ]

        return (
            "Normal",
            "Your weight is healthy. Maintain your current lifestyle.",
            foods
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
            "Grilled chicken",
            "Green tea"
        ]

        return (
            "Overweight",
            f"You should reduce about {reduce} kg to reach a healthy weight.",
            foods
        )

# ---------------- BMI API ----------------
@app.post("/bmi")
def calculate_bmi(data: BMIInput):

    weight = data.weight
    height = data.height

    # Encrypt values
    weight_enc = encrypt_value(str(weight))
    height_enc = encrypt_value(str(height))

    # Calculate BMI
    bmi = round(weight / ((height / 100) ** 2), 2)

    status, advice, foods = bmi_status(bmi, weight, height)

    # Store in database
    cursor.execute(
        """
        INSERT INTO bmi_records (weight_enc, height_enc, bmi, status, advice)
        VALUES (?, ?, ?, ?, ?)
        """,
        (weight_enc, height_enc, bmi, status, advice)
    )

    conn.commit()

    return {
        "bmi": bmi,
        "status": status,
        "advice": advice,
        "recommended_foods": foods,
        "message": "BMI calculated and stored securely"
    }

# ---------------- VIEW RECORDS ----------------
@app.get("/records")
def get_records():

    cursor.execute("SELECT id, weight_enc, height_enc, bmi, status, advice FROM bmi_records")
    rows = cursor.fetchall()

    records = []

    for row in rows:
        records.append({
            "id": row[0],
            "weight_encrypted": row[1],
            "height_encrypted": row[2],
            "bmi": row[3],
            "status": row[4],
            "advice": row[5]
        })

    return {"records": records}
