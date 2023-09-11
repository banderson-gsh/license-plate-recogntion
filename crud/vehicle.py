from typing import List
from sqlalchemy.orm import Session
from db.models import Vehicles, VehicleDetails
from schemas.models import VehicleCreate, VehicleDetailsCreate


def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicles(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def create_vehicle_details(db: Session, details: VehicleDetailsCreate):
    db_details = VehicleDetails(**details.dict())
    db.add(db_details)
    db.commit()
    db.refresh(db_details)
    return db_details


def get_all_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[Vehicles]:
    return db.query(Vehicles).order_by(Vehicles.id.desc()).offset(skip).limit(limit).all()


def get_all_vehicle_details(db: Session, skip: int = 0, limit: int = 100) -> List[VehicleDetails]:
    return db.query(VehicleDetails).group_by(VehicleDetails.vehicle_id).offset(skip).limit(limit).all()


def get_vehicle_by_plate_number(db: Session, vehicle_plate_number: str) -> Vehicles:
    return db.query(Vehicles).filter(Vehicles.plate_number == vehicle_plate_number).first()


def get_vehicle_details_by_plate_number(db: Session, vehicle_plate_number: str, skip: int = 0, limit: int = 100) -> List[VehicleDetails]:
    vehicle = get_vehicle_by_plate_number(db, vehicle_plate_number)
    return db.query(VehicleDetails).filter(VehicleDetails.vehicle_id == vehicle.id).offset(skip).limit(limit).all()
