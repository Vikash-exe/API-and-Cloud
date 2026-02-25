from fastapi import FastAPI, Path, HTTPException, Query
import json


def load_data():
    with open(r"F:\Python\FastAPI01\patients.json", "r") as file:
        data = file.read()
        return data

app = FastAPI()
@app.get("/")

def hello_world():
    return {"message": "Hello, World!"}

@app.get("/main")
def main():
    return {"message": "This is the main function of the application."}

@app.get("/view_data")
def view_data():
    data =  load_data()
    return {"data": data}

@app.get("/view_patient/{id}")
def view_data_by_id(id: str = Path(..., description="The ID of the patient to retrieve")):
    data = json.loads(load_data())
    
    if id in data:
        return{"data":data[id]}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
@app.get("/sort")
def sort_data(sort_by: str = Query(..., description="The field to sort the data by"), 
              order: str = Query('asc',description="The order to sort the data by (asc or desc)")):
    
    data = json.loads(load_data())

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid orders are: asc, desc")
    
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=False if order == 'asc' else True)
    return {"sorted_data": sorted_data}