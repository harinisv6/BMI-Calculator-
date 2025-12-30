# main.py
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# --------- DATABASE (SQLite) ----------
conn = sqlite3.connect("bmi.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    weight_enc TEXT NOT NULL,
    height_enc TEXT NOT NULL,
    bmi REAL NOT NULL,
    status TEXT NOT NULL,
    advice TEXT NOT NULL
)
""")
conn.commit()

# --------- ENCRYPTION ----------
FERNET_KEY = b'O-kN4m4NGeO9nz9JlZBCnsnPMandHr246jkURuRXVLA='
fernet = Fernet(FERNET_KEY)

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

# --------- BMI STATUS ----------
def bmi_status(bmi: float):
    if bmi < 18.5:
        return "Underweight", "You need to gain some weight"
    elif 18.5 <= bmi < 25:
        return "Normal", "You have a healthy weight. Maintain it"
    else:
        return "Overweight", "You need to lose some weight"

# --------- MODEL ----------
class BMIInput(BaseModel):
    weight: float   # kg
    height: float   # cm

# --------- API ----------
@app.post("/bmi")
def calculate_bmi(data: BMIInput):
    # Encrypt values
    weight_enc = encrypt_value(str(data.weight))
    height_enc = encrypt_value(str(data.height))

    # Calculate BMI
    bmi = round(data.weight / ((data.height / 100) ** 2), 2)

    # Get status & advice
    status, advice = bmi_status(bmi)

    # Store in SQLite
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
        "message": "BMI calculated & data stored securely"
    }

# --------- VIEW RECORDS ----------
@app.get("/records")
def get_records():
    cursor.execute("SELECT weight_enc, height_enc, bmi, status, advice FROM bmi_records")
    rows = cursor.fetchall()
    return {"records": rows}
