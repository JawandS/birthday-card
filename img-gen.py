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
from reportlab.lib.pagesizes import landscape, letter

# Constants
USE_TEST_IMAGE = False

# Function to generate image using DALL-E
def generate_image(prompt):
    # Initialize OpenAI client
    client = OpenAI()
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
    page_width, page_height = landscape(letter)
    half_page_width = page_width / 2

    c = canvas.Canvas(output_filename, pagesize=landscape(letter))

    # Resize the image to fit the left half exactly
    img_width, img_height = img.size

    # Calculate new dimensions to fill the left half completely
    new_width = half_page_width
    new_height = page_height

    # Position the image at the left half of the page
    x_pos = 0
    y_pos = 0

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        img.save(temp_file, format="PNG")
        temp_filename = temp_file.name

    # Draw the image on the left half of the page
    c.drawImage(temp_filename, x_pos, y_pos, width=new_width, height=new_height)
        
    # Add a vertical line to separate the image from the right half
    c.line(half_page_width, 0, half_page_width, page_height)
    
    # Add "Happy Birthday!" text on the right half
    # c.setFont("Helvetica-Bold", 24)
    # c.drawCentredString(page_width * 3/4, page_height / 2, "Happy Birthday!")
    
    c.showPage()
    c.save()
    
    # Clean up the temporary file
    os.unlink(temp_filename)

# Main execution
if USE_TEST_IMAGE:
    img = Image.open("temp.png")
else:
    prompt = "A vibrant birthday scene with balloons, cake, and confetti, designed to fit a vertical layout for a card."
    image_url = generate_image(prompt)
    img = process_image(image_url)
create_pdf(img, "birthday_card.pdf")

print("Birthday card generated and saved as PDF successfully!")
