# def insert(name: str, age: int):

#     if(type(name)==str and type(age)==int):
#         if(age<0):
#             raise ValueError("Age cannot be negative")
#         else:
#             print(name, age)
#     else:
#         raise TypeError("Invalid input types: name must be a string and age must be an integer")

# insert("Alice", 30)
# insert('Charlie', -5)
# insert('Bob', '25')

# Using Pydantic for data validation


from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Annotated

class Patient(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    name1: Annotated[str, Field(min_length=3, max_length=50,title= "Name of the patient",description="Name must be between 3 and 50 characters")]
    email: EmailStr
    linkedin: AnyUrl
    age: int = Field(gt=0, lt=100)
    weight: float = Field(gt=0, description="Weight must be a positive number" )
    married: Annotated[bool, Field(default=False, description="Marital status of the patient")]
    allergies: List[str] 
    contact_number: Dict[str, int]

def insert(patient: Patient):
    print(patient.name,patient.name1, patient.email, patient.age,patient.linkedin, patient.weight, patient.married, patient.allergies, patient.contact_number)

# def update(patient: Patient):
#     print(patient.name, patient.email, patient.age, patient.weight, patient.married, patient.allergies, patient.contact_number)

patient_info={'name':'Alice','name1':'Alice Smith','email':'alice1@example.com', 'linkedin':'https://www.linkedin.com/in/alice', 'age':30, 'weight':55.5,'married':False ,'allergies':['Peanuts', 'Dust'], 'contact_number':{'home':1234567890, 'work':9987654321}}

patient1=Patient(**patient_info)

insert(patient1)
# update(patient1)