import pandas as pd
import os

# Define the folder paths where CSV files are located
folders = ["certificates_courses", "degree_requirements", "majors_courses", "minors_courses", "processed_courses"]

# Function to clean the 'Credits' column
def clean_credits_column(df):
    # Replace empty values or 'N/A' with 3
    df['Credits'] = df['Credits'].replace(['N/A', ''], 3).fillna(3)
    return df

# Iterate through each folder and process all CSV files
for folder in folders:
    # Get list of all CSV files in the folder
    folder_path = f'{folder}'
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            
            # Load the CSV file
            df = pd.read_csv(file_path)
            
            # Apply the cleaning function to the 'Credits' column
            if 'Credits' in df.columns:
                df = clean_credits_column(df)
                
                # Save the cleaned DataFrame back to the file
                df.to_csv(file_path, index=False)
                print(f"Processed file: {file_path}")

print("Credits column cleaning completed for all files.")
