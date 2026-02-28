from fastapi import FastAPI, Path, HTTPException, Query
import json
from typing import Dict, List, Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError,  AnyUrl, model_validator, computed_field

class Patient(BaseModel):

    name: str
    email: EmailStr
    website:Optional[AnyUrl] = None                    
    age:int                  
    weight:float 
    height:float
    elergy:List[str]   
    contact:Dict[str, str]

    @model_validator(mode='after')
    def emergency_contact(cls, model):  #can access all the fields of the model
        contact = model.contact
        if model.age < 18 and 'emergency' not in contact:
            raise ValueError("Emergency contact is required for minors.")
        return model
    
      
    @computed_field  
    @property
    def bmi(self) -> float:

        bmi = round(self.weight / ((self.height/100) ** 2),2)  # Just a dummy formula for BMI based on height and weight
        return bmi
    
    #it is used to define a computed field that is not stored in the database but can be accessed like any other field, and it is computed based on the values of other fields in the model.

def update_patient(patient:Patient):
    print(f"Patient {patient.name} updated successfully.")
    print(f"Name: {patient.name}")
    print(f"Email: {patient.email}")
    if patient.website:
        print(f"Website: {patient.website}")
    print(f"Age: {patient.age}")
    print(f"BMI:{patient.bmi}")
    print(f"Weight: {patient.weight}")
    print(f"Allergies: {patient.elergy}")
    print(f"Contact: {patient.contact}")
    return {"message": f"Patient {patient.name} updated successfully."}

patient_info = {'name':"John Doe","email": "john.doe@gmail.com", "website": "https://www.johndoe.com", 'age':'35', 'weight':70.5, 'height':175.0, 'elergy':["Peanuts"], 'contact':{"phone": "123-456-7890"}}

patient1 = Patient(**patient_info)

update_message = update_patient(patient1)
print(update_message)