
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(default="None", max_length=50, description="The name of the patient", examples=["John Doe", "Jane Smith"])]
    email: EmailStr
    website:Optional[AnyUrl] = None # Optional field for website, default is None
    age:int = Field(default=20,gt=0) # Default age is set to 20 if not provided, and must be greater than 0
    weight:float = Field(gt=0, description="The weight of the patient in kg", strict=True) # Weight must be greater than 0
    elergy:Optional[List[str]]=Field(max_items=5) # Optional field for allergies, default is None
    contact:Dict[str, str]


    @field_validator('email')               #decorator to validate the email field easily, it will be called automatically when the model is instantiated or when the email field is updated.
    @classmethod                            
    def validate_email(cls, value):

        valid_domains = ['hdfc.com', 'gmail.com', 'yahoo.com']
        domain = value.split('@')[1]
        if domain not in valid_domains:
            raise ValueError(f"Email must be from one of the following domains: {valid_domains}")
        return value
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, name):
        return name.upper() # Convert the name to uppercase before storing it
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, age):
        if age < 18:
            raise ValueError("Patient must be at least 18 years old.")
        return age

def update_patient(patient:Patient):
    print(f"Patient {patient.name} updated successfully.")
    print(f"Name: {patient.name}")
    print(f"Email: {patient.email}")
    if patient.website:
        print(f"Website: {patient.website}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}")
    print(f"Allergies: {patient.elergy}")
    print(f"Contact: {patient.contact}")
    return {"message": f"Patient {patient.name} updated successfully."}

def insert_patient(patient:Patient):
    print(f"Patient {patient.name} inserted successfully.")
    return {"message": f"Patient {patient.name} inserted successfully."}

patient_info = {'name':"John Doe","email": "john.doe@gmail.com", "website": "https://www.johndoe.com", 'age':'35', 'weight':70.5, 'elergy':["Peanuts"], 'contact':{"phone": "123-456-7890"}}
patient1 = Patient(**patient_info)

update_message = update_patient(patient1)
print(update_message)
insert_message = insert_patient(patient1)
print(insert_message)
