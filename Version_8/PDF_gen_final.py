import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def images_to_pdf(image_paths, output_pdf):
    # Create a PDF file with A4 size
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for image_path in image_paths:
        # Open the image using Pillow
        img = Image.open(image_path)

        # Calculate the scaling factor to fit the image within the A4 page
        scaling_factor = min(letter[0] / img.width, letter[1] / img.height)

        # Calculate the new dimensions for the image
        new_width = img.width * scaling_factor
        new_height = img.height * scaling_factor

        # Calculate the centering position on the page
        x_offset = (letter[0] - new_width) / 2
        y_offset = (letter[1] - new_height) / 2

        # Draw the image onto the PDF
        c.drawInlineImage(image_path, x_offset, y_offset, width=new_width, height=new_height)

        # Add a new page for the next image (if any)
        c.showPage()

    # Save the PDF file
    c.save()

def convert_images_to_pdf(input_directory, output_pdf):
    # Get a list of all image files in the directory
    image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Sort the image files numerically based on the serial numbers in the file names
    image_files.sort(key=lambda x: int(x.split('.')[0]))

    # Create full paths for the image files
    image_paths = [os.path.join(input_directory, img) for img in image_files]

    # Call the function to convert images to PDF
    images_to_pdf(image_paths, output_pdf)


# Example usage
input_directory = os.path.join(os.path.dirname(__file__), "./PDF")
output_pdf = os.path.join(os.path.dirname(__file__), "./PDF/FinalQRcode.pdf")

convert_images_to_pdf(input_directory, output_pdf)