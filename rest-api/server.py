from fastapi import FastAPI, HTTPException, Request
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('trained_model.joblib')

# Create FastAPI app
app = FastAPI(title="House Price Prediction API", version="1.0.0")


@app.post("/predict")
async def predict(request: Request):
    try:
        # Parse JSON body directly
        features = await request.json()
        # Convert to DataFrame
        input_data = pd.DataFrame([features])
        # Make prediction
        prediction = model.predict(input_data)[0]
        # Return a response
        return {
            "prediction": float(prediction),
            "status": "success"
        }

    except Exception as e:
        # Raise HTTPException with status code 400 and error message
        raise HTTPException(status_code=400, detail=str(e))
