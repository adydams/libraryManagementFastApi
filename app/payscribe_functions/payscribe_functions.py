from telnetlib import AUTHENTICATION
import requests
from .. import schema


def get_request(request:schema.DataLookUp):
    data = request
    print(data)
    BASE_URL = "https://www.payscribe.ng/sandbox"
    authorizationVal = "Bearer ps_test_8d6767dfd157243104362b2988f8080c4b12b3728bed2dedab817f9d2820364e"
    headers =  {'content-type': 'application/json', 'Authorization': authorizationVal }
    
    r = requests.post(url=BASE_URL, data=data, headers=headers)
    
