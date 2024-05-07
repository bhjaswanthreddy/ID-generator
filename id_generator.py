from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import io
import csv
import os

# Define the file paths
TEMPLATE_IMAGE = "id_template.jpg"  # Ensure this is the correct path to your ID template image
DATA_CSV = "employee_data.csv"      # Update this to the correct path of your CSV file
PHOTOS_DIR = "photos"               # Directory where employee photos are stored
OUTPUT_PDF = "employee_ids.pdf"     # The output file name for the PDF


def create_id_page(template_image, name, title, photo_path):
    with Image.open(template_image) as template, Image.open(photo_path).resize((150, 200)) as photo:
        template.paste(photo, (50, 50))  # Adjust position as needed
        return template.convert('RGB')  # Convert to RGB and ensure it is a fresh copy

def main():
    output = PdfWriter()  # Use PdfWriter

    with open(DATA_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            photo_path = os.path.join(PHOTOS_DIR, row['photo'])
            # Ensure image creation and handling is done within a context where the file is open
            with create_id_page(TEMPLATE_IMAGE, row['name'], row['title'], photo_path) as id_page:
                img_bio = io.BytesIO()  # Create a BytesIO object
                id_page.save(img_bio, 'PDF', resolution=100.0)  # Save image to BytesIO object as PDF
                img_bio.seek(0)  # Reset stream position

                # Read the PDF from BytesIO using PdfReader
                pdf_page = PdfReader(img_bio)
                output.add_page(pdf_page.pages[0])  # Add the page using add_page method

    with open(OUTPUT_PDF, 'wb') as outfile:
        output.write(outfile)

if __name__ == "__main__":
    main()
