from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import os

def convert_images_to_pdf(image_paths, output_pdf_path):
    pdf_canvas = canvas.Canvas(output_pdf_path, pagesize=A4)

    for image_path in image_paths:
        image = Image.open(image_path)
        
        # Calculate scaling factors to fit the image within the A4 page
        width_ratio = A4[0] / image.width
        height_ratio = A4[1] / image.height
        scaling_factor = min(width_ratio, height_ratio)
        
        # Calculate position to center the image on the page
        x_offset = (A4[0] - image.width * scaling_factor) / 2
        y_offset = (A4[1] - image.height * scaling_factor) / 2
        
        # Draw the image on the PDF canvas
        pdf_canvas.drawImage(ImageReader(image), x_offset, y_offset,
                             width=image.width * scaling_factor, height=image.height * scaling_factor)
        
        pdf_canvas.showPage()  # Move to the next page

    pdf_canvas.save()

if __name__ == "__main__":
    input_dir = os.path.join(os.path.dirname(__file__), "./PDF_generation")
    output_pdf_path = os.path.join(os.path.dirname(__file__),"./PDF_generation/Final_output.pdf")
    
    # Get a list of all items (files and folders) in the folder
    all_items = os.listdir(input_dir)

    # Filter out only the files from the list
    file_list = [item for item in all_items if os.path.isfile(os.path.join(input_dir, item))]


    # Sort the file list in serial order
    image_files = sorted(file_list, key=lambda x: int(x.split('.')[0]))

    image_paths = [os.path.join(input_dir, filename) for filename in image_files]
    
    convert_images_to_pdf(image_paths, output_pdf_path)
