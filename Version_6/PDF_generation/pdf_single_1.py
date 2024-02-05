from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from PIL import Image

def create_pdf(qr_folder, phonetics_folder, output_pdf):
    qr_images = sorted(os.listdir(qr_folder))
    phonetics_images = sorted(os.listdir(phonetics_folder))

    pdf = canvas.Canvas(output_pdf, pagesize=letter)

    for qr_image, phonetics_image in zip(qr_images, phonetics_images):
        qr_path = os.path.join(qr_folder, qr_image)
        phonetics_path = os.path.join(phonetics_folder, phonetics_image)

        qr_image = Image.open(qr_path)
        phonetics_image = Image.open(phonetics_path)

        # Calculate scaling factors to fit the images within the PDF page
        qr_scale_factor = min(float(letter[0]) / qr_image.width, float(letter[1]) / qr_image.height)
        phonetics_scale_factor = min(float(letter[0]) / phonetics_image.width, float(letter[1]) / phonetics_image.height)

        pdf.pagesize = (letter[0], letter[1])

        pdf.drawInlineImage(qr_path, 0, 0, width=qr_image.width * qr_scale_factor, height=qr_image.height * qr_scale_factor)
        pdf.showPage()

        pdf.drawInlineImage(phonetics_path, 0, 0, width=phonetics_image.width * phonetics_scale_factor, height=phonetics_image.height * phonetics_scale_factor)
        pdf.showPage()

    pdf.save()


if __name__ == "__main__":
    qr_folder_path = os.path.join(os.path.dirname(__file__), "./QR_codes")
    phonetics_folder_path = os.path.join(os.path.dirname(__file__), "./Phonetics")
    output_pdf_path = "output_resize.pdf"

    create_pdf(qr_folder_path, phonetics_folder_path, output_pdf_path)
