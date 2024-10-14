import os
import re
import pandas as pd

# Folder paths
input_folder = 'degree_requirements'
output_folder = 'prdr'

# Ensure the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to clean the description by removing words and keeping only numerical values
def clean_description(description):
    # Remove everything that's not a number, period, or whitespace (keeps numerical values like "3", "120", "2.0", etc.)
    cleaned_description = ' '.join(re.findall(r'\d+\.?\d*', description))
    return cleaned_description

# Loop through all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):  # Only process CSV files
        input_file_path = os.path.join(input_folder, file_name)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file_path)

        # Check if 'Category' and 'Description' columns exist
        if 'Category' in df.columns and 'Description' in df.columns:
            
            # Remove the 'Major' and 'URL' columns if they exist
            if 'Major' in df.columns:
                df = df.drop(columns=['Major'])
            if 'URL' in df.columns:
                df = df.drop(columns=['URL'])
            
            # Clean the 'Description' column to retain only numerical values
            df['Description'] = df['Description'].apply(clean_description)

            # Ensure only 'Category' and 'Description' columns are left
            df = df[['Category', 'Description']]

            # Save the processed file to the output folder
            output_file_path = os.path.join(output_folder, file_name)
            df.to_csv(output_file_path, index=False)

            print(f"Processed file saved: {output_file_path}")
        else:
            print(f"Skipping {file_name}: 'Category' or 'Description' column not found.")

print(f"All files in '{input_folder}' have been processed and saved to '{output_folder}'.")
