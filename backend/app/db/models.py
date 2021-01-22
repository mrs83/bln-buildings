from sqlalchemy import Boolean, Column, Integer, String, Date

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Building(Base):
    __tablename__ = "building"

    adressid = Column(Integer, primary_key=True, index=True)
    objectid = Column(Integer, index=True)
    bez_name = Column(String)
    ort_name = Column(String)
    plr_name = Column(String)
    str_name = Column(String)
    hnr = Column(Integer)
    plz = Column(Integer, index=True)
    blk = Column(Integer)
    adr_datum = Column(Date)
    str_datum = Column(Date)
    qualitaet = Column(String)
    typ = Column(String)
