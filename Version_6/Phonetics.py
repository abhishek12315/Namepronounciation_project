import pandas as pd
import os

def generate_phonetic_spelling(name):
    phonetic_components = {
        'a': 'ah',
        'e': 'eh',
        'i': 'ee',
        'o': 'oh',
        'u': 'oo',
    }
    
    name = name.lower()
    
    phonetic_spelling = ''
    for char in name:
        if char in phonetic_components:
            phonetic_spelling += phonetic_components[char] + '-'
        else:
            phonetic_spelling += char
    
    return phonetic_spelling


### UMID 8 DIGIT TEXT CONVERTED USING THIS FORMULA IN EXCEL "=TEXT(A1, "00000000")"
file_path = pd.read_excel(os.path.join(os.path.dirname(__file__), "./JSONs/Student_info.xlsx"), dtype={"UMID": str}, header=0)  # Replace with the path to your Excel file
df = pd.read_excel(file_path)

df['Full name'] = df['First Name'] + ' ' + df['Last Name']

df['Phonetics'] = df['Full name'].apply(generate_phonetic_spelling)
df.to_excel(file_path, index=False, engine='openpyxl')

print("Phonetic spellings have been generated and stored in the Excel file.")