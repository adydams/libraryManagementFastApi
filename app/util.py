from jose import JWTError, jwt
from passlib.context import CryptContext
import pandas as pd
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

def update_password(old_plain_password, hash_password, new_plain_password):
    return pwd_context.verify_and_update(old_plain_password, hash_password, new_plain_password )

def convertBytesToString(bytes):
    #data = bytes.decode('utf-8').split()
    # df = pd.DataFrame(data)
    df = pd.read_excel(bytes)
    # df.loc[0]
    # print(df)
    return parse_csv(df)

def parse_csv(df):
    result = df.to_json(orient = "records")
    parsed = json.loads(result)
    return parsed

