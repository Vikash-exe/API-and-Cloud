import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field, ValidationError, field_validator
import json
import pandas as pd
import pickle
from typing import List, Optional, Literal, Annotated
from fastapi.responses import JSONResponse



#importing the user_input module from the schema package to use the UserInput class for data validation and processing
import schema.user_input 


#impoting the model
with open(r"F:\Python\FastAPI01\API-and-Cloud\Insurance Risk Premium Predictor\model.pkl", "rb") as file:
    model = pickle.load(file)

model_version = "1.0.0"

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Health Premier Risk Prediction API. Use the /predict endpoint to get your health risk category based on your details."}

@app.get("/health")
def health_check():
    return {
        "status": "API is healthy and running.",
        "version": model_version,
        "model loaded": model is not None
        }

@app.post("/predict")
def predict_risk(data: schema.user_input.UserInput):

    input_df = pd.DataFrame ([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "tier": data.tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
        
    }])

    try:
        prediction = model.predict(input_df)[0]
        return JSONResponse(status_code=200, content={"risk_category": prediction})
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": tb})


    


