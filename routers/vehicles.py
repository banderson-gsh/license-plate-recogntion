from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import base64
from crud import vehicle as crud_vehicle
from core.dependencies import get_db
from schemas.models import VehicleCreate, VehicleInDB, VehicleDetailsCreate, VehicleDetailsInDB
from utils.anpr import send_to_anpr

router = APIRouter()

@router.post("/create-vehicle/", response_model=VehicleInDB)
async def create_vehicle(vehicle_details: VehicleDetailsCreate, db: Session = Depends(get_db)):
    try:
        if vehicle_details.image is None:
            raise HTTPException(status_code=400, detail="Base 64 encoded image not provided!")

        if vehicle_details.gps_details is None:
            raise HTTPException(status_code=400, detail="GPS details are not provided!")

        encoded_image_data = vehicle_details.image.split(',')[1]
        license_number = await send_to_anpr(image_data=encoded_image_data)

        if license_number is None:
            raise HTTPException(status_code=400, detail="Plate number not retrieved!")

        db_vehicle = crud_vehicle.get_vehicle_by_plate_number(db, vehicle_plate_number=license_number)

        if not db_vehicle:
            new_vehicle = crud_vehicle.create_vehicle(db, vehicle=VehicleCreate(plate_number=license_number))            
            if not new_vehicle:
                raise HTTPException(status_code=400, detail="Failed to create vehicle!")

            new_vehicle_details = crud_vehicle.create_vehicle_details(db, details=VehicleDetailsCreate(image=encoded_image_data, gps_details=vehicle_details.gps_details, vehicle_id=new_vehicle.id))            
            if not new_vehicle_details:
                raise HTTPException(status_code=400, detail="Failed to create vehicle details!")

            return new_vehicle

        new_vehicle_details = crud_vehicle.create_vehicle_details(db, details=VehicleDetailsCreate(image=encoded_image_data, gps_details=vehicle_details.gps_details, vehicle_id=db_vehicle.id))

        if not new_vehicle_details:
            raise HTTPException(status_code=400, detail="Failed to create vehicle details!")

        return db_vehicle

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicles-list/", response_model=List[VehicleInDB])
def get_vehicles_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        vehicles_list = crud_vehicle.get_all_vehicles(db, skip=skip, limit=limit)
        return vehicles_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicles/{vehicle_plate_number}/", response_model=VehicleInDB)
def get_vehicle(vehicle_plate_number: str, db: Session = Depends(get_db)):
    try:
        vehicle = crud_vehicle.get_vehicle_by_plate_number(db, vehicle_plate_number=vehicle_plate_number)
        
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found!")
        return vehicle

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicles/{vehicle_plate_number}/details/", response_model=List[VehicleDetailsInDB])
def get_specific_vehicle_details(vehicle_plate_number: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        specific_vehicle_details = crud_vehicle.get_vehicle_details_by_plate_number(db, vehicle_plate_number=vehicle_plate_number, skip=skip, limit=limit)

        if not specific_vehicle_details:
            raise HTTPException(status_code=404, detail="Specific vehicle details not found!")
        return specific_vehicle_details

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

