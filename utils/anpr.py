import httpx
import base64
from core.config import settings
import logging
from urllib.parse import urlencode, urljoin

logging.basicConfig(level=logging.INFO)

async def send_to_anpr(image_data: str):
    basic_auth = base64.b64encode(f"{settings.ANPR_API_USER}:{settings.ANPR_API_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "text/plain"
    }
    
    parameters = {
        'region': 'EU',
        'topn': 10,
        'confidence': 400
    }
    
    query_string = urlencode(parameters)
    full_url = urljoin(settings.ANPR_API_ENDPOINT, f"?{query_string}")
    
    payload = image_data
    license_number = None

    async with httpx.AsyncClient() as client:
        try:
            logging.info(f"Sending request to {full_url} with headers {headers} and payload {payload[:500]}...")
            response = await client.post(full_url, data=payload, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            logging.info("response_json:", response_json)

            if response_json.get("vehicle") and len(response_json["vehicle"]) > 0:
                license_number = response_json["vehicle"][0]["plate"]["license"]
            else:
                license_number = None
                
            return license_number
        
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            logging.error(f"Request error occurred: {e}")
        except ValueError as e:
            logging.error(f"Recognition failure: {e}")
            
