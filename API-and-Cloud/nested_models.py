from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    email: str
    age: int
    address: Address

address_info = {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip_code": "12345"}
patient_info = {"name": "John Doe", "email": "john.doe@example.com", "age": 30, "address": address_info}

address = Address(**address_info)
patient1 = Patient(**patient_info)
print(patient1)

temp = patient1.model_dump()  #for converting the model to a dictionary
temp = patient1.model_dump_json(exclude={'address': ['street', 'city']}, exclude_none=True,exclude_unset=True)  # Exclude the 'street' and 'city' fields from the 'address' field, and exclude any fields that have a value of None. and exclude any fields that have not been set (i.e., fields that have their default value). This is useful for creating a JSON representation of the model that only includes the relevant information, and excludes any unnecessary or sensitive data.
print(temp)
print(type(temp))  #easier for debugging, as it allows you to see the structure of the data and how it is being represented in JSON format.