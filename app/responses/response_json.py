from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ConfigError

def response_json(message: str, status: int = 200)-> JSONResponse:
    return JSONResponse(content={"message":message}, status_code= status)