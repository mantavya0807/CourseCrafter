import os
import pandas as pd

# Folder paths
input_folder = 'newprdr'
output_folder = 'hope'

# Ensure the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to process each DataFrame
def process_df(df):
    # Remove the 'Cultures Requirement' row
    df = df[df['Category'] != 'Cultures Requirement']
    
    # Create new rows for 'US Culture' and 'International Culture'
    new_rows = pd.DataFrame({
        'Category': ['US Culture', 'International Culture'],
        'Description': ['3', '3']
    })

    # Append the new rows to the DataFrame
    df = pd.concat([df, new_rows], ignore_index=True)

    return df

# Loop through all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):  # Only process CSV files
        input_file_path = os.path.join(input_folder, file_name)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file_path)

        # Process the DataFrame (remove 'Cultures Requirement' and add 'US Culture' and 'International Culture')
        df = process_df(df)

        # Save the processed file to the output folder
        output_file_path = os.path.join(output_folder, f'{file_name}')
        df.to_csv(output_file_path, index=False)

        print(f"Processed file saved: {output_file_path}")

print(f"All files in '{input_folder}' have been processed and saved to '{output_folder}'.")
