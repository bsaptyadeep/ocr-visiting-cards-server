from fastapi import FastAPI, File, UploadFile
from PIL import Image
import cloudinary
import cloudinary.uploader
from io import BytesIO
import pytesseract
from dotenv import load_dotenv
import os

# Set Tesseract path explicitly
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure Cloudinary
cloudinary.config(
    cloud_name = "saptya", 
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET"), # Click 'View API Keys' above to copy your API secret
    secure=True
)

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.post("/process-visiting-card-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Open image
        image = Image.open(file.file)
        width, height = image.size
        
        # Define grid size (2x5)
        rows, cols = 5, 2
        grid_width, grid_height = width // cols, height // rows
        
        uploaded_urls = []
        
        # Split and upload each part
        for row in range(rows):
            for col in range(cols):
                left = col * grid_width
                upper = row * grid_height
                right = left + grid_width
                lower = upper + grid_height
                cropped_img = image.crop((left, upper, right, lower))
                
                extracted_text = pytesseract.image_to_string(cropped_img).strip()


                # Save to bytes
                img_bytes = BytesIO()
                cropped_img.save(img_bytes, format="PNG")
                img_bytes.seek(0)

                # Upload to Cloudinary
                response = cloudinary.uploader.upload(img_bytes, folder="image_slices/")

                # Collect URL
                uploaded_urls.append({
                    "url": response.get("secure_url"),
                    "ocr-metadata": extracted_text
                })

        return {"image_urls": uploaded_urls}
    
    except Exception as e:
        return {"error": str(e)}
