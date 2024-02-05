from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(qr_folder, phonetics_folder, output_pdf):
    qr_images = sorted(os.listdir(qr_folder))
    phonetics_images = sorted(os.listdir(phonetics_folder))

    pdf = canvas.Canvas(output_pdf, pagesize=letter)

    for qr_image, phonetics_image in zip(qr_images, phonetics_images):
        qr_path = os.path.join(qr_folder, qr_image)
        phonetics_path = os.path.join(phonetics_folder, phonetics_image)

        pdf.drawInlineImage(qr_path, 0, 0, width=letter[0], height=letter[1])
        pdf.showPage()

        pdf.drawInlineImage(phonetics_path, 0, 0, width=letter[0], height=letter[1])
        pdf.showPage()

    pdf.save()

if __name__ == "__main__":
    qr_folder_path = os.path.join(os.path.dirname(__file__), "./QR_codes")
    phonetics_folder_path = os.path.join(os.path.dirname(__file__), "./Phonetics")
    output_pdf_path = "output.pdf"

    create_pdf(qr_folder_path, phonetics_folder_path, output_pdf_path)
