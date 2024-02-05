import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

import barcode
from barcode.writer import ImageWriter

class QRCodeGenerator:
    def __init__(self):
        self.credentials_path = None

    # Generate a barcode
    def generate_barcode(self, umid, barcode_format):
        """
        Generate barcode image and save it to a file
        :param data: Data to be encoded in the barcode
        :param barcode_format: Barcode format (e.g., 'ean13', 'code39')
        """
        # Create a barcode object
        barcode_class = barcode.get_barcode_class(barcode_format)
        barcode_instance = barcode_class(umid, writer=ImageWriter())

        # Save the barcode image to a file
        barcode_instance.save(os.path.join(os.path.dirname(__file__), f"../Barcodes/{umid}"))

        print(f'Barcode saved as {umid}.png')

    def insert_newline(self, sentence, max_length):
        words = sentence.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_length:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        # Add the last line
        lines.append(current_line.strip())

        return lines

    def generate_qr_code_image(self, umid, full_name, phonetics):
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=11,
            border=3,
        )

        # Add data to the QR code
        qr.add_data(umid)
        qr.make(fit=True)

        # Create a QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Calculate image dimensions at 96 DPI
        dpi = 96
        img_width = int(4.25 * dpi)
        img_height = int(5.5 * dpi)
        border_size = 8  # Border size in pixels

        # Create a blank image with the specified dimensions
        img = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(img)

        # Paste the QR code in the center of the image
        qr_width, qr_height = qr_img.size
        qr_position = ((img_width - qr_width) // 2, (img_height - qr_height - 100) // 2)
        img.paste(qr_img, qr_position)

        ScanMe_font_size = 22
        ScanMe_font = ImageFont.truetype("arialbd.ttf", ScanMe_font_size)  # You may need to adjust the font path
        ScanMe_name = f"Scan Me!!!"
        full_name_width, full_name_height = draw.textsize(ScanMe_name, ScanMe_font)
        full_name_position = ((img_width - full_name_width) // 2, qr_position[1]-10)
        draw.text(full_name_position, ScanMe_name, font=ScanMe_font, fill="black")


        # Add student full name at the bottom, centered align
        full_name_font_size = 30
        full_name_font = ImageFont.truetype("arialbd.ttf", full_name_font_size)  # You may need to adjust the font path
        full_name1 = self.insert_newline(full_name, max_length=21)
        for i in range(len(full_name1)):
            if i == 0:
                full_name_width, full_name_height = draw.textsize(full_name1[i], full_name_font)
                full_name_position = ((img_width - full_name_width) // 2, qr_position[1] + qr_height)
                draw.text(full_name_position, full_name1[i], font=full_name_font, fill="black")
            else:
                full_name_width, full_name_height = draw.textsize(full_name1[i], full_name_font)
                full_name_position = ((img_width - full_name_width) // 2, full_name_position[1]+30)
                draw.text(full_name_position, full_name1[i], font=full_name_font, fill="black")

        # Add student phonetics below full name
        phonetics_font_size = 20
        phonetics_font = ImageFont.truetype("arial.ttf", phonetics_font_size)
        phonetics1 = self.insert_newline(phonetics, max_length=38)
        for i in range(len(phonetics1)):
            if i == 0:
                phonetics_width, phonetics_height = draw.textsize(phonetics1[i], phonetics_font)
                phonetics_position = ((img_width - phonetics_width) // 2, full_name_position[1] + 40)
                draw.text(phonetics_position, phonetics1[i], font=phonetics_font, fill="black")
            else:
                phonetics_width, phonetics_height = draw.textsize(phonetics1[i], phonetics_font)
                phonetics_position2 = ((img_width - phonetics_width) // 2, phonetics_position[1] + 20)
                draw.text(phonetics_position2, phonetics1[i], font=phonetics_font, fill="black")

        # Add a border around the entire image
        draw.rectangle([(0, 0), (img_width - 1, img_height - 1)], outline="black", width=border_size)

        # Save or show the generated image
        # img.save(f"{umid}_qrcode.png")
        # img.show()
        local_path = os.path.join(os.path.dirname(__file__), f"./{umid}.jpg")
        img.save(local_path, format='JPEG')


