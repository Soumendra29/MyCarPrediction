from pathlib import Path
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "Frontend"
MODEL_PATH = BASE_DIR / "model.pkl"
COLUMNS_PATH = BASE_DIR / "columns.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
SCALE_COLS_PATH = BASE_DIR / "scale_cols.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(COLUMNS_PATH, "rb") as f:
    model_columns = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

with open(SCALE_COLS_PATH, "rb") as f:
    scale_cols = pickle.load(f)

app = FastAPI(title="MyCarPrediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OWNER_MAPPING = {
    "First Owner": 1,
    "Second Owner": 2,
    "Third Owner": 3,
    "Fourth & Above Owner": 4,
    "Test Drive Car": 0,
}


def build_input_row(year, kms, owner_text, fuel, seller, transmission,
                    mileage, engine, max_power, seats):
    owner = OWNER_MAPPING.get(owner_text, 0)
    row = {column: 0 for column in model_columns}

    # Numeric fields
    for field, val in [
        ("year", year),
        ("km_driven", kms),
        ("owner", owner),
        ("mileage", mileage),
        ("engine", engine),
        ("max_power", max_power),
        ("seats", seats),
    ]:
        if field in row:
            row[field] = val

    # Categorical fields
    feature_map = {
        f"fuel_{fuel}": 1,
        f"seller_type_{seller}": 1,
        f"transmission_{transmission}": 1,
    }
    for feature_name, value in feature_map.items():
        if feature_name in row:
            row[feature_name] = value

    return row


@app.post("/api/predict")
async def api_predict(request: Request):
    try:
        form = await request.form()

        Year = int(form.get("Year", 0))
        Kms_Driven = int(form.get("Kms_Driven", 0))
        Owner = form.get("Owner", "")
        Fuel_Type = form.get("Fuel_Type", "")
        Seller_Type = form.get("Seller_Type", "")
        Transmission = form.get("Transmission", "")
        Mileage = float(form.get("Mileage", 15.0))
        Engine = float(form.get("Engine", 1200.0))
        Max_Power = float(form.get("Max_Power", 80.0))
        Seats = float(form.get("Seats", 5.0))

        input_row = build_input_row(
            Year, Kms_Driven, Owner, Fuel_Type, Seller_Type, Transmission,
            Mileage, Engine, Max_Power, Seats
        )
        input_df = pd.DataFrame([input_row], columns=model_columns)

        # Scale karo
        input_df[scale_cols] = scaler.transform(input_df[scale_cols])

        prediction = model.predict(input_df)[0]
        predicted_price = round(float(np.expm1(prediction)), 0)

        return {"success": True, "prediction": predicted_price}

    except Exception as exc:
        return JSONResponse(status_code=400, content={"success": False, "error": str(exc)})


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)