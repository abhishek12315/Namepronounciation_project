import pandas as pd
import os
import json

# Load the Excel sheet containing the emails
excel_df = pd.read_excel(os.path.join(os.path.dirname(__file__), f"./JSONs/Student_info.xlsx"))

# Load the JSON data containing a list of email addresses
with open(os.path.join(os.path.dirname(__file__), f"./JSONs/No_Audio_file.json"), 'r') as file:
    json_emails = json.load(file)

# Create a DataFrame with the email addresses from the JSON
json_df = pd.DataFrame({'Email': json_emails})

# Filter the Excel data based on the email addresses from the JSON
filtered_excel_data = excel_df[excel_df['Email'].isin(json_df['Email'])]

# Save the filtered data to a new Excel file
filtered_excel_data.to_excel(os.path.join(os.path.dirname(__file__), f"./JSONs/filtered_data.xlsx"), index=False)
