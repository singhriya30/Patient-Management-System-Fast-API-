from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Annotated

class Patient(BaseModel):
    name : str
    email : EmailStr
    age : int       
    weight : float
    married : bool
    allergies : List[str]
    contact_number : Dict[str, int]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']

        domain = value.split('@')[-1]

        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value.upper()

def update(patient: Patient):
    print(patient.name, patient.email, patient.age, patient.weight, patient.married, patient.allergies, patient.contact_number)

patient_info={'name':'Bob','email':'bob@hdfc.com','age':30,'weight':70.5,'married':True,'allergies':['peanuts'],'contact_number':{'home':1234567890}}
patient1=Patient(**patient_info)
update(patient1)