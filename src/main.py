from fastapi import FastAPI,UploadFile, File, Depends
import pandas as pd
from typing import Union
from io import BytesIO
from sqlalchemy.orm import Session
from .database import get_db
from .models import Data_Stunting
from .response import OK,NOT_FOUND,UNAUTHORIZED
from .middleware import tokenCheck
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

auth_scheme = HTTPBearer()
app = FastAPI()
tc = TestClient(app)

@app.get('/')
def index():
    return {"Hello":"Python"}

@app.get('/protected',dependencies=[Depends(tokenCheck),Depends(auth_scheme)])
def protectedRoute():
    return {"Hello":"Python"}

@app.get('/stunting',dependencies=[Depends(tokenCheck),Depends(auth_scheme)],tags=["Data"], summary='Get all available data')
def stunting(db: Session = Depends(get_db)):
    result = db.query(Data_Stunting).all()
    return OK(result)

@app.get('/stunting/kabupaten-kota/{id}', tags=["Data"])
async def getSingleData(id:int, db: Session = Depends(get_db)):
    result = db.query(Data_Stunting).filter(Data_Stunting.kode_kabupaten_kota == id).all();
    if result != None and len(result) != 0:
        return OK(result)
    else:
        return NOT_FOUND()

@app.post('/upload-bulk', tags=["Data"])
def insert_bulk(file: UploadFile = File(...),db: Session = Depends(get_db)):
    added = 0
    updated = 0
    contents = file.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    for r in df.itertuples():
        isExist = db.query(Data_Stunting).filter(Data_Stunting.kode_kabupaten_kota == r.kode_kabupaten_kota, Data_Stunting.tahun == r.tahun).first()
        if isExist == None:
            added = added + 1
            newRow = Data_Stunting(
                kode_provinsi = r.kode_provinsi,
                nama_provinsi = r.nama_provinsi,
                kode_kabupaten_kota = r.kode_kabupaten_kota,
                nama_kabupaten_kota = r.nama_kabupaten_kota,
                jumlah_balita_stunting = r.jumlah_balita_stunting,
                satuan = r.satuan,
                tahun = r.tahun,
            )
            db.add(newRow)
            db.commit()
        else:
            updated = updated + 1
            isExist.jumlah_balita_stunting = r.jumlah_balita_stunting
            db.commit()
    data.close()
    file.file.close()
    return {"result":{"added":added,"updated":updated}}
