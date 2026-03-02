from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from typing import Optional, Annotated
from pydantic import BaseModel, Field, computed_field
import os

# Configuration: parameterized file path
DATA_FILE_PATH = os.getenv("PATIENTS_DATA_PATH", r"F:\Python\FastAPI01\patients.json")


class Patient(BaseModel):

    id: Annotated[str , Field(..., description="The ID of the patient", examples=['P001', 'P002'])]
    name : Annotated[str , Field(..., description="The name of the patient", examples=["John Doe", "Jane Smith"])]
    city : Annotated[str , Field(..., description="The city of the patient", examples=["New York", "Los Angeles"])]
    age  : Annotated[int , Field(..., gt=0, description="The age of the patient", examples=[30, 40])]
    gender : Annotated[str, Field(..., description="The gender of the patient",)]
    height : Annotated[float , Field(..., gt=0, description="The height of the patient in cm", examples=[175.0, 160.0])]
    weight : Annotated[float , Field(..., gt=0, description="The weight of the patient in kg", examples=[70.5, 60.0])]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height) ** 2),2)  # formula for BMI based on height and weight
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(None, description="The name of the patient", examples=["John Doe", "Jane Smith"])] = None
    city : Annotated[Optional[str], Field(None, description="The city of the patient", examples=["New York", "Los Angeles"])] = None
    age  : Annotated[Optional[int], Field(None, gt=0, description="The age of the patient", examples=[30, 40])] = None
    gender : Annotated[Optional[str], Field(None, description="The gender of the patient", examples=["Male", "Female"])] = None
    height : Annotated[Optional[float], Field(None, gt=0, description="The height of the patient in cm", examples=[175.0, 160.0])] = None
    weight : Annotated[Optional[float], Field(None, gt=0, description="The weight of the patient in kg", examples=[70.5, 60.0])] = None

app = FastAPI()

@app.put("/update_patient/{id}")
def patient_update(id:str, patient: PatientUpdate):   #will create object of PatientUpdate class and validate the data. id is passed as path parameter and patient is passed as request body

    data = json.loads(load_data())

    if id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient = data[id]  # Get the existing patient data from the dictionary

    patient_update_value = patient.model_dump(exclude_unset=True)  # Convert the update data to a dictionary while excluding unset fields
    
    existing_patient.update(patient_update_value)  # Update the existing patient data with the new values
    
    # Adding the id back and validate with Pydantic
    existing_patient['id'] = id
    patient_pydantic_object = Patient(**existing_patient)  # Create a new Patient object to validate the updated data for bmi and verdict calculations as well as other field validations
    existing_patient = patient_pydantic_object.model_dump(exclude=['id'])  # Convert the validated Patient object back to a dictionary, excluding id
    
    data[id] = existing_patient  # Update the patient data in the main data dictionary
    save_data(data)  # Save the updated data back to the file
    
    return JSONResponse(status_code=200,content={"message": f"Patient {id} updated successfully."})
        

def load_data():
    with open(DATA_FILE_PATH, "r") as file:
        data = file.read()
        return data
    
def save_data(data):
    with open(DATA_FILE_PATH, "w") as file:
        json.dump(data, file)

@app.get("/")

def hello_world():
    return {"message": "Hello, World!"}


@app.get("/view_patient/{id}")
def view_data_by_id(id: str = Path(..., description="The ID of the patient to retrieve")):
    data = json.loads(load_data())

    if id in data:
        return {"data": data[id]}

    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/add_patient")
def add_patient(patient: Patient):
    data = json.loads(load_data())

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={"message": f"Patient {patient.name} added successfully."} )

@app.delete("/delete_patient/{id}")
def delete_patient(id: str):
    data = json.loads(load_data())
    if id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": f"Patient {id} deleted successfully."})

