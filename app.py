#This will serve as our main file for the application

# import asyncio
# import aiohttp
import uvicorn
from fastapi import FastAPI, Request
import json
import os
import sys
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.datastructures import MutableHeaders
from functions.user import *
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from functions.messages import *
from functions.encryption import *
#from functions.dbconnect import *

templates = Jinja2Templates(directory="webpages")
app = FastAPI()


app.mount("/webpages", StaticFiles(directory="webpages"), name="static")

@app.route('/', methods=['GET'])
async def index(request: Request):
    return templates.TemplateResponse("coming_soon/index.html", {"request": request})

@app.get('/user/register')
async def user_register(email: str, password: str, name: str, surname: str, birthdate: str, phone_number = None, city = None, country = None):
    data = await user_create(email, password, name, surname, birthdate, phone_number, city, country)
    if data is None:
        msgl = {
            'msg': "User successfully created!"
        }
    else:
        msgl = {
            'msg': "User already exists!"
        }
    data = jsonable_encoder(msgl)
    return JSONResponse(content=data)


@app.get('/user/remove')
async def user_remove(email: str, password: str):
    data = await user_delete(email, password)
    if data is None:
        msgl = {
            'msg': "User successfully deleted!"
        }
    else:
        msgl = {
            'msg': "User does not exist!"
        }
    data = jsonable_encoder(msgl)
    return JSONResponse(content=data)


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
