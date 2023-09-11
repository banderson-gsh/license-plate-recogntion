from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import base64
from crud import vehicle as crud_vehicle
from core.dependencies import get_db
from schemas.models import VehicleCreate, VehicleInDB, VehicleDetailsCreate, VehicleDetailsInDB
from utils.compression import compress_image
from utils.anpr import send_to_anpr


router = APIRouter()

@router.post("/create-vehicle/", response_model=VehicleInDB)
async def create_vehicle(file: UploadFile = File(...), gps_details: str = None, db: Session = Depends(get_db)):
    try:
        compressed_image = await compress_image(await file.read())
        plate_number = await send_to_anpr(compressed_image)
        image_base64 = base64.b64encode(compressed_image).decode()

        db_vehicle = crud_vehicle.get_vehicle_by_plate_number(db, vehicle_plate_number=plate_number)

        if db_vehicle:
            vehicle_details_data = VehicleDetailsCreate(image=image_base64, gps_details=gps_details, vehicle_id=db_vehicle.id)
            new_vehicle_details = crud_vehicle.create_vehicle_details(db, details=vehicle_details_data)

            if not new_vehicle_details:
                raise HTTPException(status_code=400, detail="Failed to create vehicle details!")

        else:
            vehicle_data = VehicleCreate(plate_number=plate_number)
            new_vehicle = crud_vehicle.create_vehicle(db, vehicle=vehicle_data)

            if new_vehicle:
                vehicle_details_data = VehicleDetailsCreate(image=image_base64, gps_details=gps_details, vehicle_id=new_vehicle.id)
                new_vehicle_details = crud_vehicle.create_vehicle_details(db, details=vehicle_details_data)

                if not new_vehicle_details:
                    raise HTTPException(status_code=400, detail="Failed to create vehicle details!")

            else:
                raise HTTPException(status_code=400, detail="Failed to create vehicle!")

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

