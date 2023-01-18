from sqlalchemy import Integer,String
from sqlalchemy.sql.schema import Column
from .database import Base

class Data_Stunting(Base):
    __tablename__ = 'data_stunting'

    id = Column(Integer, primary_key=True)
    kode_provinsi = Column(Integer)
    nama_provinsi = Column(String)
    kode_kabupaten_kota = Column(Integer)
    nama_kabupaten_kota = Column(String)
    jumlah_balita_stunting = Column(Integer)
    satuan = Column(String)
    tahun = Column(Integer)