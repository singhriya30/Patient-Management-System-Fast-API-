from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="Unique identifier for the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient", min_length=3, max_length=50, examples=['Alice Smith'])]
    city: Annotated[str, Field(..., description="City of the patient", examples=['New York'])]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0,lt=100, examples=[25])]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient", examples=['Female'])]
    height: Annotated[float, Field(..., description="Height of the patient in cm", ge=0, examples=[170.5])]
    weight: Annotated[float, Field(..., description="Weight of the patient in kg", ge=0, examples=[68.2])]

    @computed_field
    @property
    def bmi(self) -> float:
        height_in_meters = self.height / 100
        bmi = round(self.weight / (height_in_meters ** 2), 2)
        return bmi

    @computed_field
    @property
    def Verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"  
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    with open('patients.json', 'r') as f:
        data =json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
        

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')

    # if not, add the new patient to the data and save it back to the file
    data[patient.id]= patient.model_dump(exclude=['id'])

    # save the updated data back to the file
    save_data(data)

    return JSONResponse(status_code=201, content={'Message': 'Patient created successfully', 'patient_id': patient.id})


@app.put('/Edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data= load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_data = data[patient_id]
    updated_patient_info= patient_update.model_dump(exclude_unset= True)

    for key, value in updated_patient_info.items():
        existing_patient_data[key]= value


    #existing_patient_data -> pydantic object-> update bmi or vardict
    existing_patient_data['id']= patient_id
    patient_pydantic_object= Patient(**existing_patient_data)

    #pydantic object-> dict
    existing_patient_data= patient_pydantic_object.model_dump(exclude="id")

    #add this dictionary to data
    data[patient_id]= existing_patient_data

    #save the updated data back to the file
    save_data(data)

    return JSONResponse(status_code=200, content={'Message': 'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data= load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'Message': 'Patient deleted successfully'})