import qrcode
from PIL import ImageDraw, ImageFont, Image
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from smtplib import SMTPAuthenticationError

# read the email address and password from environment variables
email_address = "labissf@gmail.com"
email_password = "ozviuxfitfoqtofo" # Mail specific password. 

try: 
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()
    smtp_server.login(email_address, email_password)
except SMTPAuthenticationError as e:
    print("Failed to authenticate with the SMTP server:", e)
    

#%%
class QRCodeUploader:
    def __init__(self):
        self.credentials_path = None

    def generate_qr_code(self, Name, umid):
        qr = qrcode.QRCode(version=1, box_size=48, border=4)
        qr.add_data(umid)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_width, qr_height = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arialbd.ttf", 100)
        label_text = f"Scan Me!!"
        label_width, label_height = draw.textsize(label_text, font=font)
        label_position = ((qr_width - label_width) // 2, qr_height - label_height - 10)
        draw.text(label_position, label_text, font=font, fill="black")
        img = img.resize((1200, 1500), Image.ANTIALIAS)
        return img
    
    def generate_phonetics(self, Full_Name, Phonetics, umid):
        # Create a new image with white background
        width, height = 1200, 1350
        phon_image = Image.new('RGB', (width, height), 'white')
           
           # Load a font
        font = ImageFont.truetype("arialbd.ttf", 72)  # You can specify a different font if needed
           
           # Draw the Full_Name on the image
        draw = ImageDraw.Draw(phon_image)
        name_position = ((width - draw.textlength(Full_Name, font)) / 2, 675)
        draw.text(name_position, Full_Name, fill='black', font=font)
           
           # Draw the phonetics below Full_Name
        phonetics_position = ((width - draw.textlength(Phonetics, font)) / 2, 775)
        draw.text(phonetics_position, Phonetics, fill='black', font=font)
        return phon_image

        
    def send_email(self, email, img):
        # create the message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = email
        msg['Subject'] = 'Test Email'
        
        # add the image as a link
        body = "Please check out your QR code image!"
        msg.attach(MIMEText(body, 'html'))
        
        # add the image as an attachment
        #image_path = os.path.join('H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/QR codes', '63402444.png')

        img = MIMEImage(img)
        img.add_header('Content-Disposition', 'attachment', filename='QR_code.jpg')
        msg.attach(img)
        
        # Path to the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), "../JSONs/sent_emails.json")

        # Load existing email addresses from the JSON file
        try:
            with open(json_file_path, 'r') as file:
                file_content = file.read()
                if file_content:
                    sent_emails = json.loads(file_content)
                else:
                    sent_emails = []
        except FileNotFoundError:
            # If the JSON file doesn't exist, initialize an empty list
            sent_emails = []
        
        # send the message
        try:
            if email in sent_emails:
                print(f"Skipping email to {email}. Already sent.")
            else:
                smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
                print(f"Email sent to {email}")
                sent_emails.append(email)
                with open(json_file_path, "w") as file:
                    json.dump(sent_emails, file)
        except Exception as e:
            print(f"Error sending email to {email}: {e}")
