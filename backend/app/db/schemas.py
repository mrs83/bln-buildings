from datetime import datetime
from pydantic import BaseModel
import typing as t


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


class BuildingBase(BaseModel):
    adressid: int
    objectid: int
    bez_name: str
    ort_name: str
    plr_name: str
    str_name: str
    hnr: int
    plz: int
    blk: t.Optional[int] = None
    adr_datum: t.Optional[datetime] = None
    str_datum: datetime
    qualitaet: str
    typ: str


class BuildingOut(BuildingBase):
    pass


class Building(BuildingBase):
    class Config:
        orm_mode = True
