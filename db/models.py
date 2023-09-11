from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


# Users model
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))


# Vehicles schema
class Vehicles(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True)
    vehicle_details = relationship("VehicleDetails", back_populates="vehicle")


# Vehicle Details schema
class VehicleDetails(Base):
    __tablename__ = "vehicle_details"
    
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    gps_details = Column(String)
    vehicle_id = Column(Integer, ForeignKey(Vehicles.id))
    
    vehicle = relationship("Vehicles", back_populates="vehicle_details")

