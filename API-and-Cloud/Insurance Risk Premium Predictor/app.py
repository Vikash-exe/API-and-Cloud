import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field, ValidationError, field_validator
import pandas as pd
from typing import List, Literal, Annotated
from fastapi.responses import JSONResponse
from model.predict import model, model_version, predict_output
from schema.prediction_category import prediction_response


#importing the user_input module from the schema package to use the UserInput class for data validation and processing
import schema.user_input 

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

@app.post("/predict", response_model=prediction_response)
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
        prediction = predict_output(input_df)
        return JSONResponse(status_code=200, content={"Prediction": prediction})
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": tb})


    


