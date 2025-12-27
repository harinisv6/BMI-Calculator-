from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from cryptography.fernet import Fernet

app = FastAPI()

# DB CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="bmi_app"
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
