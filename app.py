#!/usr/bin/python

# imports
import uvicorn
import os
import psutil
from datetime import datetime
from fastapi import FastAPI
from fastapi import Request
from fastapi import Form
from fastapi import Response
from fastapi import UploadFile
from mod.utils import render_picture, encode_bs64
from mod.db import global_init
from mod.api import API

# Create server
app = FastAPI()

# Record server start time (UTC)
server_started = datetime.now()

# Init database
global_init("database.db")


# Server home page
@app.get('/')
def home_page(request: Request):
    return {'hello': 'world'}


# Server page with working statistics
@app.get('/status')
def status_page(request: Request):
    ram = psutil.virtual_memory()
    stats = {
        "Server time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Server uptime": str(datetime.now()-server_started),
        "CPU": f"{psutil.cpu_count()} cores ({psutil.cpu_freq().max}MHz) with {psutil.cpu_percent()} current usage",
        "RAM": f"{ram.used >> 20} mb / {ram.total >> 20} mb"
    }
    return stats


# get user
@app.get('/get_user/{id}')
def get_user(request: Request, id):
    return API.get_user(id)


# create user
@app.post('/create_user/')
def create_user(
        request: Request,
        name: str = Form(),
        email: str = Form()):
    return API.create_user(name, email)


# get mem
@app.get('/get_mem/{id}')
def get_mem(request: Request, id):
    return API.get_mem(id)


# create mem
@app.post('/create_mem/')
def create_mem(
        file: UploadFile,
        request: Request,
        title: str = Form(),
        text: str = Form(),
        tag: str = Form(),
        id: str = Form(),
        token: str = Form()):
    if not file:
        return {"message": "No upload file sent"}
    bs4 = render_picture(file.file.read())
    return API.create_mem(title, text, bs4, token, tag, id)


# get mem image
@app.get('/get_mem_image/{id}')
def get_mem_image(request: Request, id):
    img = encode_bs64(API.get_mem(id).image)
    return Response(content=img, media_type="image/png")


# get hot mems
@app.get('/get_hot/{a}/{b}')
def get_hot(request: Request, a, b):
    return API.get_hot_mems(a, b)


# Start server
if __name__ == "__main__":
    uvicorn.run('app:app',
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        log_level="debug",
        http="h11",
        reload=True,
        use_colors=True,
        workers=3
    )
