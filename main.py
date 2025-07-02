from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json
app = FastAPI()

class Patients(BaseModel):
    id: Annotated[str,Field(..., description='please enter patient id',example='P002')]
    name: Annotated[str,Field(...,description='please enter patient name',example='saqib')]
    city: Annotated[str,Field(...,description='please enter city name',example='gujranwala')]
    age: Annotated[int,Field(...,description='enter age between 20 and 90',gt=20,lt=90)]
    gender: Annotated[Literal['male','female','others'],Field(...,description='enter gender male,female or others')]
    height: Annotated[float,Field(...,description='please enter eight in meters ',example=25)]
    weight: Annotated[float,Field(...,description='enter your weight in kgs',example='67.5')]
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight/self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi<20:
            verdict = 'under weight'
        elif self.bmi>20 and self.bmi<50:
            verdict= 'average weight'
        elif self.bmi>50:
            verdict='overweight' 
        return verdict







def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
@app.get('/')
def hello():
    return {'helo':'world'}

@app.post('/patient_entry')
def patient(pat:Patients):
    data = load_data()
    if pat.id in data:
        raise HTTPException(status_code=404,detail='patient already exists')
    else:
       data[pat.id]=pat.model_dump(exclude=['id']) #model.dum is converting our data recieved from http into dictionary and is stored in a new key (data[id])
    save_data(data)


