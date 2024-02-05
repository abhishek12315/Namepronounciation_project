import pandas as pd
import numpy as np
import os
from Utils_classes.FunctionQrcodegen import QRCodeGenerator

# student_data = pd.read_excel(os.path.join(os.path.dirname(__file__), "./JSONs/1student_list.xlsx"), dtype={"UMID": str}, header=0)

# student_data.dropna(subset=["Email", "UMID"], inplace=True)
# umids = np.array(student_data.loc[:, "UMID"])
# Full_Names = np.array(student_data.loc[:, "Diploma Name"])
# Phonetics = np.array(student_data.loc[:, "Phonetics"])

# qr_uploader = QRCodeGenerator()
# count = 0
# for umid, Full_Name, Phonetic in zip(umids, Full_Names, Phonetics):
#     qr_img = qr_uploader.generate_qr_code_image(umid, Full_Name, Phonetic)
  
#     count += 1

# print(count)

qr_uploader = QRCodeGenerator()
# Example usage
data = '80992868'
barcode_format = 'ean8'  # EAN-13 format
qr_uploader.generate_barcode(data, barcode_format)