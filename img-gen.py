#######################################################
# Generate an image using the Stable Diffusion pipeline
# and save it as a PDF file
# 
# Author: Jawand Singh
#
# Date: 2024-30-12
#######################################################

# Dependencies
import tempfile
import os
from openai import OpenAI
import requests
from PIL import Image
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Initialize OpenAI client
client = OpenAI()

# Function to generate image using DALL-E
def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    return image_url

# Function to download and process image
def process_image(image_url):
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    return img

# Function to create PDF with the image
def create_pdf(img, output_filename):
    # Standard US Letter size
    page_width = 8.5 * inch
    page_height = 11 * inch
    
    # Calculate dimensions for half a page
    half_page_height = page_height / 2
    
    # Create PDF
    c = canvas.Canvas(output_filename, pagesize=(page_width, page_height))
    
    # Calculate scaling factor to fit image on half the page
    img_width, img_height = img.size
    scale_factor = min(page_width / img_width, half_page_height / img_height)
    
    # Calculate new dimensions
    new_width = img_width * scale_factor
    new_height = img_height * scale_factor
    
    # Calculate position to center the image
    x_centered = (page_width - new_width) / 2
    y_centered = (page_height - new_height) / 2
    
    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        img.save(temp_file, format="PNG")
        temp_filename = temp_file.name
    
    # Draw the image on the PDF
    c.drawImage(temp_filename, x_centered, y_centered, width=new_width, height=new_height)
    
    c.showPage()
    c.save()
    
    # Clean up the temporary file
    os.unlink(temp_filename)

# Main execution
prompt = "A serene landscape with mountains and a lake at sunset"
image_url = generate_image(prompt)
img = process_image(image_url)
create_pdf(img, "generated_image.pdf")

print("Image generated and saved as PDF successfully!")
