FROM python:3.9

WORKDIR /license_plate_recognition_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
