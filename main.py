from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from torch_snippets import *
import json
import os
from io import BytesIO

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/files", StaticFiles(directory="files"), name="files")
templates = Jinja2Templates(directory="templates")

from src.core import im2id
def load_image_into_numpy_array(data): return np.array(Image.open(BytesIO(data)))

@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post('/uploaddata/')
async def upload_file(request: Request, file:UploadFile=File(...)):
    print(request)
    content = file.file.read()
    saved_filepath = f'files/{file.filename}'
    with open(saved_filepath, 'wb') as f:
        f.write(content)
    im = read(saved_filepath)
    output = im2id(im)
    payload = {'request': request, 
        "filename": file.filename, 
        'output': output}
    return templates.TemplateResponse("home.html", payload)

@app.post("/predict")
async def predict(request: Request, file:UploadFile=File(...)):
    content = file.file.read()
    image = Image.open(io.BytesIO(content)).convert('L')
    output = im2id(im)
    return output