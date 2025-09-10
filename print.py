import pandas as pd

# File path to the Excel file
file_path = 'data1.xlsx'  # Update the path if needed

# Read the Excel file
try:
    df = pd.read_excel(file_path, engine='openpyxl')
except Exception as e:
    print(f"Error reading the Excel file: {e}")
    raise

first_row = df.iloc[0].to_dict()

for i in range(1, len(first_row)):  # Assuming there are 29 attributes
    attribute_name_col = f'Attribute {i} name'
    attribute_value_col = f'Attribute {i} value(s)'
    
    if attribute_name_col in first_row and attribute_value_col in first_row:
        attribute_name = first_row[attribute_name_col]
        attribute_value = first_row[attribute_value_col]
        print(f"{attribute_name} : {attribute_value}")
print("\n")  # Print a newline for better readability between rows
