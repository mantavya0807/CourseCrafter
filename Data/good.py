import os
import pandas as pd

# Path to the folder containing the CSV files
input_folder = "Majors_Course_Plans"
output_folder = "Major_Course_Plans_Transformed"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define a mapping for Year and Semester to a numeric sequence
year_semester_map = {
    "First Year Fall": 1,
    "First Year Spring": 2,
    "Second Year Fall": 3,
    "Second Year Spring": 4,
    "Third Year Fall": 5,
    "Third Year Spring": 6,
    "Fourth Year Fall": 7,
    "Fourth Year Spring": 8
}

# Process each CSV file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        # Load the CSV file
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)

        # Combine Year and Semester into one numeric value
        df['Year_Semester'] = df['Year'] + ' ' + df['Semester']
        df['Year_Semester'] = df['Year_Semester'].map(year_semester_map)



        # Replace 'or', 'and', ',' with '||' and '&&'
        df['Course'] = df['Course'].str.replace(',', '||').str.replace(' or ', '||').str.replace(' and ', '&&')

        # Drop the old Year and Semester columns
        df.drop(columns=['Year', 'Semester'], inplace=True)

        # Rename columns for clarity
        df.rename(columns={'Year_Semester': 'Semester_Number'}, inplace=True)

        # Save the transformed file in the output folder
        output_file_path = os.path.join(output_folder, f"transformed_{filename}")
        df.to_csv(output_file_path, index=False)

        print(f"Processed and saved {filename} as {output_file_path}")
