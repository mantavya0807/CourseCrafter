import os
import pandas as pd

# Folder paths
input_folder = 'prdr'
output_folder = 'newprdr'

# Ensure the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to refine specific values based on the 'Category' column
def refine_values(category, description):
    if "Limitations on Source and Time for Credit Acquisition" in category:
        return '24'
    elif "First Year Engagement" in category:
        return '1-3'
    elif "Total Minimum Credits" in category:
        return '120'
    elif "Cultures Requirement" in category:
        return '6'
    elif "US Culture" in category:
        return '3'
    elif "International Culture" in category:
        return '3'
    else:
        return description  # Keep the original value for other categories

# Loop through all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):  # Only process CSV files
        input_file_path = os.path.join(input_folder, file_name)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file_path)
        
        # Check if the necessary columns ('Category' and 'Description') exist
        if 'Category' in df.columns and 'Description' in df.columns:
            
            # Apply the refinement function to the 'Description' column
            df['Description'] = df.apply(lambda row: refine_values(row['Category'], row['Description']), axis=1)

            # Ensure only 'Category' and 'Description' columns are present
            df = df[['Category', 'Description']]

            # Save the processed file to the output folder
            output_file_path = os.path.join(output_folder, f'{file_name}')
            df.to_csv(output_file_path, index=False)

            print(f"Processed file saved: {output_file_path}")
        else:
            print(f"Skipping {file_name}: 'Category' or 'Description' column not found.")

print(f"All files in '{input_folder}' have been processed and saved to '{output_folder}'.")
