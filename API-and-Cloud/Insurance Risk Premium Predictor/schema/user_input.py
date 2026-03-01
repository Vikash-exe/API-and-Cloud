from logging import config

from pydantic import BaseModel, Field, computed_field, field_validator
import typing

from config.city import tier1, tier2

class UserInput(BaseModel):
    age: typing.Annotated[int, Field(..., gt=0, description="The age of the user", examples=[30, 40])]
    weight:typing.Annotated[float, Field(..., gt = 0, description="The weight of the user in kg", examples=[70.5, 60.0])]
    height: typing.Annotated[float, Field(..., gt = 0,lt=2.5, description="The height of the user in cm", examples=[170.0, 165.5])]
    income_lpa: typing.Annotated[float, Field(..., ge=0, description="The income level of the user in LPA", examples=[10000, 25000])]
    smoker: typing.Annotated[bool, Field(..., description="Whether the user is a smoker", examples=[True, False])]
    city: typing.Annotated[str, Field(..., description="The city of the user", examples=["New York", "Los Angeles"])]
    occupation: typing.Annotated[typing.Literal['retired', 'freelancer', 'student', 'government_job',
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
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, value):
        return value.strip().title()
    