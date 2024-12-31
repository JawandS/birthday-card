#######################################################
# Generate an image using the Stable Diffusion pipeline
# and save it as a PDF file
# 
# Author: Jawand Singh
#
# Date: 2024-30-12
#######################################################

# Dependencies
import datetime
import tempfile
import os
from os.path import join as mkpath
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
    # save image with timestamp as filename
    img.save(mkpath("imgs", f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"))
    return img

# Function to create PDF with the image
def create_pdf(img, output_filename, target_name):
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
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_width * 3/4, page_height / 2, f"Happy Birthday {target_name}!")
    
    c.showPage()
    c.save()
    
    # Clean up the temporary file
    os.unlink(temp_filename)

def create_birthday_prompt(attributes):
    age = attributes.get('age')
    if not age:
        raise ValueError("Age must be provided")

    base_prompt = f"A vibrant birthday scene for a {age}-year-old"
    
    if 'gender' in attributes:
        base_prompt += f" {attributes['gender']}"
    
    base_prompt += ", designed in a vertical layout for a card"
    
    if 'interests' in attributes and attributes['interests']:
        interests = attributes['interests']
        interest_string = ", ".join(interests[:-1]) + f" and {interests[-1]}" if len(interests) > 1 else interests[0]
        base_prompt += f", featuring elements related to {interest_string}"
    
    if 'style' in attributes:
        base_prompt += f", in a {attributes['style']} style"
    
    if 'color_scheme' in attributes:
        base_prompt += f", using a {attributes['color_scheme']} color scheme"
    
    base_prompt += ". Include birthday cake, balloons, and appropriate decorations."
    
    return base_prompt

# Main execution
if USE_TEST_IMAGE:
    img = Image.open("temp.png")
else:
    # Create prompt
    attributes = {
        'age': 30,
        'gender': 'woman',
        'interests': ['travel', 'photography', 'cats'],
        'style': 'watercolor',
        'color_scheme': 'pastel',
        'name': 'Alice'
    }
    prompt = create_birthday_prompt(attributes)
    # Generate image
    image_url = generate_image(prompt)
    img = process_image(image_url)
create_pdf(img, "birthday_card.pdf", target_name=attributes['name'])

print("Birthday card generated and saved as PDF successfully!")
