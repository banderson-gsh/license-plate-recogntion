import httpx
import base64
from core.config import settings

async def send_to_anpr(image_data: bytes):
    basic_auth = base64.b64encode(f"{settings.ANPR_API_USER}:{settings.ANPR_API_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }

    payload = {
        "image": base64.b64encode(image_data).decode()
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(settings.ANPR_API_ENDPOINT, json=payload, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            plate_number = response_json.get("vehicle")["plate"]["license"] if response_json.get("vehicle") else None
            return plate_number
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
        except ValueError as e:
            print(f"Recognition failure: {e}")

