from PIL import Image
import io

def compress_image(image_data: bytes, quality: int = 85) -> bytes:
    try:
        image = Image.open(io.BytesIO(image_data))
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=quality)
        return buffered.getvalue()
    except Exception as e:
        print("An error occurred while compressing the image:", str(e))
        return b''
