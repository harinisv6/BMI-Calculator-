
import os
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# DB
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306))
)
cursor = db.cursor()

# ENCRYPTION
FERNET_KEY = b'O-kN4m4NGeO9nz9JlZBCnsnPMandHr246jkURuRXVLA='
fernet = Fernet(FERNET_KEY)

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

# MODEL
class BMIInput(BaseModel):
    weight: float   # kg
    height: float   # meters

# API
@app.post("/bmi")
def calculate_bmi(data: BMIInput):
    # Encrypt values
    weight_enc = encrypt_value(str(data.weight))
    height_enc = encrypt_value(str(data.height))
# BMI calculation
    bmi = data.weight / ((data.height/100) ** 2)
# Store encrypted data + bmi
    query = """
    INSERT INTO bmi_records (weight_enc, height_enc, bmi)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (weight_enc, height_enc, round(bmi, 2)))
    db.commit()

    return {
        "bmi": round(bmi, 2),
        "message": "BMI calculated & data stored securely"
    }
