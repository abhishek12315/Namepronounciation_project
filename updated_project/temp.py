import pandas as pd
import numpy as np

emails_df = pd.read_excel("./updated_project/Student_info.xlsx")

# Locate the row based on the target cell value
row = emails_df.loc[emails_df['UMID'] == 67938153]

# Access the entire row
selected_row = emails_df.loc[row.index]

Name = selected_row.at[row.index[0], 'Full name']

# Print the selected row
print(str(Name))

