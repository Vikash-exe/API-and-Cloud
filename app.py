import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field, ValidationError
import json
import pandas as pd
import pickle
from typing import List, Optional, Literal, Annotated
from fastapi.responses import JSONResponse

#impoting the model
with open(r"F:\Python\FastAPI01\model.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()

tier1 = ['Delhi','Mumbai','Bangalore','Hyderabad','Kolkata',]
tier2 = ['Jaipur', 'Chennai', 'Indore', 'Kota', 
'Chandigarh', 'Pune',  'Lucknow', 'Gaya',
'Jalandhar', 'Mysore']

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, description="The age of the user", examples=[30, 40])]
    weight:Annotated[float, Field(..., gt = 0, description="The weight of the user in kg", examples=[70.5, 60.0])]
    height: Annotated[float, Field(..., gt = 0,lt=2.5, description="The height of the user in cm", examples=[170.0, 165.5])]
    income_lpa: Annotated[float, Field(..., ge=0, description="The income level of the user in LPA", examples=[10000, 25000])]
    smoker: Annotated[bool, Field(..., description="Whether the user is a smoker", examples=[True, False])]
    city: Annotated[str, Field(..., description="The city of the user", examples=["New York", "Los Angeles"])]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="The occupation of the user", examples=["Engineer", "Teacher"])]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height)**2),2)
        return bmi
    
    @computed_field
    @property
    def age_group(self)-> str:
         if self.age < 25:
            return "young"
         elif self.age < 45:
            return "adult"
         elif self.age<60:
            return "middle_age"
         else:
            return "senior"
         

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.bmi > 30 and self.smoker:
            return "high"
        elif self.bmi > 27 and self.smoker:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def tier(self) -> int:
        if self.city in tier1:
            return 1
        elif self.city in tier2:
            return 2
        return 3
    
@app.post("/predict")
def predict_risk(data: UserInput):

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


    


