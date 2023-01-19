from fastapi import FastAPI, UploadFile, File, Depends
import pandas as pd
from typing import Union
from io import BytesIO
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .database import get_db, engine
from .models import Data_Stunting
from .response import OK, NOT_FOUND, UNAUTHORIZED
from .middleware import tokenCheck
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

auth_scheme = HTTPBearer()
app = FastAPI()
tc = TestClient(app)


@app.get('/', tags=['GENERAL'])
def index():
    return {"Sampurasun": "Wargi jabar"}


@app.get('/protected', dependencies=[Depends(tokenCheck), Depends(auth_scheme)], tags=['GENERAL'], summary='End Point for Testing Purpose')
def protectedRoute():
    return {"Hello": "I am protected"}


@app.get('/stunting', dependencies=[Depends(tokenCheck), Depends(auth_scheme)], tags=["DATA PROVIDER"], summary='Get all available stunting case data in jawa barat')
def stunting(db: Session = Depends(get_db)):
    result = db.query(Data_Stunting).all()
    return OK(result)


@app.get('/stunting/kabupaten-kota/{id}', dependencies=[Depends(tokenCheck), Depends(auth_scheme)], tags=["DATA PROVIDER"], summary='Get number of stunting case for certain kabupaten/kota')
async def getSingleData(id: int, db: Session = Depends(get_db)):
    result = db.query(Data_Stunting).filter(
        Data_Stunting.kode_kabupaten_kota == id).all()
    if result != None and len(result) != 0:
        return OK(result)
    else:
        return NOT_FOUND()


@app.get('/stunting/jumlah-kasus/', dependencies=[Depends(tokenCheck), Depends(auth_scheme)], tags=["DATA PROVIDER"], summary='Get total summary of stunting case on yearly period')
async def getDataByTahun():
    with engine.connect() as con:
        result = con.execute(
            "SELECT SUM(jumlah_balita_stunting) as total_kasus, tahun FROM data_stunting GROUP BY tahun").fetchall()
        return OK(result, message='Data jumlah kasus balita terkena stunting berdasarkan tahun di jawa barat')


@app.get('/stunting/kasus-tertinggi/tahun', dependencies=[Depends(tokenCheck), Depends(auth_scheme)], tags=["DATA PROVIDER"], summary='Get list of kabupaten/kota with higest stunting case by year')
async def getKasusTerparahByTahun():
    with engine.connect() as con:
        result = con.execute('SELECT t1.total_kasus,t2.nama_kabupaten_kota, t1.tahun FROM (SELECT MAX(jumlah_balita_stunting) as total_kasus,tahun FROM data_stunting GROUP BY tahun) t1 INNER JOIN (SELECT jumlah_balita_stunting, nama_kabupaten_kota FROM data_stunting) t2 ON t1.total_kasus = t2.jumlah_balita_stunting').fetchall()
        return OK(result, message='Data kabupaten/kota dengan jumlah balita penderita stunting tertinggi setiap tahunnya')


@app.post('/upload-bulk', tags=["DATA COLLECTOR"], summary='End point for upload csv file to update the database')
def insert_bulk(file: UploadFile = File(...), db: Session = Depends(get_db)):
    added = 0
    updated = 0
    contents = file.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    for r in df.itertuples():
        isExist = db.query(Data_Stunting).filter(Data_Stunting.kode_kabupaten_kota ==
                                                 r.kode_kabupaten_kota, Data_Stunting.tahun == r.tahun).first()
        if isExist == None:
            added = added + 1
            newRow = Data_Stunting(
                kode_provinsi=r.kode_provinsi,
                nama_provinsi=r.nama_provinsi,
                kode_kabupaten_kota=r.kode_kabupaten_kota,
                nama_kabupaten_kota=r.nama_kabupaten_kota,
                jumlah_balita_stunting=r.jumlah_balita_stunting,
                satuan=r.satuan,
                tahun=r.tahun,
            )
            db.add(newRow)
            db.commit()
        else:
            updated = updated + 1
            isExist.jumlah_balita_stunting = r.jumlah_balita_stunting
            db.commit()
    data.close()
    file.file.close()
    return {"result": {"added": added, "updated": updated}}
