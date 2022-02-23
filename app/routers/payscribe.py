from typing import Optional
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, HttpUrl
import requests
from ..payscribe_functions.payscribe_functions import get_request
from ..  import schema
import pandas as pd
from decouple import config


#when passing the data directly
#check in .env file
router = APIRouter(
    prefix = "/payscribe",
    tags=['Payscribe']
)

url = "https://www.payscribe.ng/sandbox"
authorizationVal = config('authorizationVal')

headers =  {'content-type': 'application/json', 'Authorization': authorizationVal }
   

@router.post("/datalookup/")
def data_look_up(request: schema.DataLookUp):
    data = request.network
    
    r =  requests.post(url= f"{url}/data/lookup/", data = { "network" : data  }, headers=headers)
    #print (r.status_code)
    #print(r.json().get('message').get('details'))
    return r.json()

@router.post("/datavend/")
def data_vend(request: schema.DataVend):
    
    data ={
        "plan" : request.plan,
        "recipent" : pd.to_numeric( request.recipent, errors='coerce'),
        "network" : request.network
    }
    r = requests.post(url= f"{url}/data/vend", data = {
        "plan" : request.plan,
        "recipent" : request.recipent,
        "network" : request.network
        } , headers=headers)
    print(r.json())
    return r.json()