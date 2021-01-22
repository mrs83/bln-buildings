from fastapi import HTTPException, status
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_buildings(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.BuildingOut]:
    return db.query(models.Building).offset(skip).limit(limit).all()


def create_building(db: Session, building: schemas.Building, update: bool = False):
    db_building = db.query(models.Building).filter_by(adressid=building.adressid).one_or_none()
    if db_building and not update:
        return db_building

    if not update:
        db_building = models.Building(
            adressid=building.adressid,
            objectid=building.objectid,
            bez_name=building.bez_name,
            ort_name=building.ort_name,
            plr_name=building.plr_name,
            str_name=building.str_name,
            hnr=building.hnr,
            plz=building.plz,
            blk=building.blk,
            adr_datum=building.adr_datum,
            str_datum=building.str_datum,
            qualitaet=building.qualitaet,
            typ=building.typ
        )
    else:
        update_data = building.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_building, key, value)
    
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def get_total_buildings_by_plz(db: Session, plz: int = None):
    count_ = func.count('*').label('total')
    query = db.query(models.Building.plz, count_)
    if plz:
        query = query.filter(models.Building.plz == plz)
    query = query.group_by(models.Building.plz).order_by(count_.desc())
    return [{'plz': r[0], 'total': r[1]} for r in query.all()]


def get_total_buildings_by_year(db: Session, plz: int = None):
    count_ = func.count('*').label('total')
    year_ = extract('year', models.Building.str_datum)
    query = db.query(year_, count_)
    if plz:
        query = query.filter(models.Building.plz == plz)
        query = query.group_by(year_, models.Building.plz)
    else:
        query = query.group_by(year_)
    query = query.order_by(count_.desc())
    return [{'year': r[0], 'total': r[1]} for r in query.all()]
