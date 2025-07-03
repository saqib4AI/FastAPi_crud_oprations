from fastapi import FastAPI,HTTPException,Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
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


@app.get('/retrieve_patient/{patient_id}')
def retrieve(patient_id:str = Path(...,description='enter patient id to retrieve patient data',examples='P001')):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient does not exist with this id')
    else:
        return data[patient_id]
    






@app.post('/Create_patient_entry')
def patient(pat:Patients):
    data = load_data()
    if pat.id in data:   # here data is same as data.keys()
        raise HTTPException(status_code=404,detail='patient already exists')
    else:
       data[pat.id]=pat.model_dump(exclude=['id']) #model.dum is converting our data recieved from http into dictionary and is stored in a new key (data[id])
    save_data(data)




class Update_model(BaseModel):
    name: Annotated[Optional[str],Field(default=None,description='please update name',example='saqib')]
    city: Annotated[Optional[str],Field(default=None,description='please enter updated city name',example='gujranwala')]
    age:  Annotated[Optional[int],Field(default=None,description='enter current age',gt=20,lt=90)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None,description='enter gender male,female or others')]
    height:Annotated[Optional[float],Field(default=None,description='please update height in meters ',example=25.5)]
    weight:Annotated[Optional[float],Field(default=None,description='update your weight in kgs',example=67.5)]


@app.put('/update_patient_record/{patient_id}')
def update(patient_id:str, obj:Update_model):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='please enter correct id')
    else:
                
        model_obj_dic =obj.model_dump(exclude_unset=True)
        old_data = data[patient_id]
        for key,value in model_obj_dic.items():
            old_data[key] = value
        # we have copied new incmoing values to old data,now old data is updated.but there were values
        #like bmi which were dependent on weight and height ....also to be changed.code is under below
        old_data['id'] = patient_id

        new_obj = Patients(**old_data) # dictionary unpacking,bcs pydantic model does not accepts dictionary.
        final_data = new_obj.model_dump(exclude='id')
        data[patient_id]=final_data  
    save_data(data)
    #return {"message": "patient data updated"}

    return JSONResponse(status_code = 200, content={'message':'patient data updated'})

@app.delete('/delete_record/{patient_id}')
def delete_record(patient_id:str):
    data = load_data()
    if patient_id not in data:
        return HTTPException(status_code=404,detail='patient does not exist')
    else:
        del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient is deleted'})
    



    


