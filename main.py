# main.py
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# --------- DATABASE (SQLite) ----------
conn = sqlite3.connect("bmi.db", check_same_thread=False)
cursor = conn.cursor()

# Create table without id or created_at
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    weight_enc TEXT NOT NULL,
    height_enc TEXT NOT NULL,
    bmi REAL NOT NULL
)
""")
conn.commit()

# --------- ENCRYPTION ----------
FERNET_KEY = b'O-kN4m4NGeO9nz9JlZBCnsnPMandHr246jkURuRXVLA='
fernet = Fernet(FERNET_KEY)

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

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
    bmi = data.weight / ((data.height / 100) ** 2)

    # Store in SQLite
    cursor.execute(
        "INSERT INTO bmi_records (weight_enc, height_enc, bmi) VALUES (?, ?, ?)",
        (weight_enc, height_enc, round(bmi, 2))
    )
    conn.commit()

    return {
        "bmi": round(bmi, 2),
        "message": "BMI calculated & data stored securely"
    }

# Optional: view all records (encrypted)
@app.get("/records")
def get_records():
    cursor.execute("SELECT * FROM bmi_records")
    rows = cursor.fetchall()
    return {"records": rows}
