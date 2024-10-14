import os
import pandas as pd

# Path to the folder containing the CSV files (majors_courses2)
input_folder = 'majors_courses2'  # Update this to the path of your input majors folder

# Output folder for the updated files (majors)
output_folder = 'majors'  # Specify the output folder for the modified CSVs
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each CSV file in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        input_csv_path = os.path.join(input_folder, file_name)

        # Load the CSV into a DataFrame
        df = pd.read_csv(input_csv_path)
        print(df.columns)
        
        # Check if the 'Type' column exists
        if 'Type' not in df.columns:
            print(f"'Type' column not found in {file_name}. Skipping this file.")
            continue

        # Find all distinct types (A, B, C, etc.) in the 'Type' column
        distinct_types = df['Type'].dropna().unique()

        # Loop through each distinct type (A, B, C, etc.)
        for course_type in distinct_types:
            # Filter rows where 'Type' matches the current course_type
            df_group = df[df['Type'] == course_type].copy()

            # Check if there are any courses of this type to process
            if df_group.empty:
                print(f"No '{course_type}' type courses found in {file_name}. Skipping...")
                continue

            # Combine the course codes from rows where 'Type' is the current type
            combined_course_codes = '|'.join(df_group['Course_Code'].dropna())

            # Get the value from 'Credits_Required' for the current type (assuming all have the same value)
            try:
                credits_required = df_group['Credits_Required'].astype(float).dropna().iloc[0]
            except (IndexError, ValueError):
                print(f"No valid 'Credits_Required' values found for {course_type} in {file_name}. Skipping this group.")
                continue

            # Calculate how many times to repeat the new row (credits_required / 3)
            num_repeats = int(credits_required / 3)

            # Create a new row with combined course codes, Mandatory = 1, and other details
            new_row = {
                'Major': df_group['Major'].iloc[0],  # Use the first major value
                'Course_Code': combined_course_codes,  # Combined course codes
                'Course_Title': '',  # Empty title for combined row
                'Credits': credits_required,  # Credits required from calculation
                'Mandatory': 1 if course_type == 'A' else 0,  # Set Mandatory to 1 for 'A', 0 for others
                'Select': 1 if course_type != 'A' else 0,  # Selectable if not 'A'
                'Academic_Plan': 1,  # Assuming Academic Plan 1 for now
                'year': df_group['year'].iloc[0] if 'year' in df_group.columns else '',  # Year if available
                'semester': df_group['semester'].iloc[0] if 'semester' in df_group.columns else '',  # Semester if available
                'URL': df_group['URL'].iloc[0]  # Use the first URL (assuming it's the same for all)
            }

            # Create a DataFrame with the new row repeated
            df_new_rows = pd.DataFrame([new_row] * num_repeats)

            # Define output CSV path
            output_csv_path = os.path.join(output_folder, file_name)  # Saving in 'majors' folder

            # Check if the file already exists
            if os.path.exists(output_csv_path):
                # If the file exists, append without the header
                df_new_rows.to_csv(output_csv_path, mode='a', header=False, index=False)
            else:
                # If the file doesn't exist, write with the header
                df_new_rows.to_csv(output_csv_path, mode='w', header=True, index=False)

            print(f"Processed and added new data for '{course_type}' in: {file_name} to the 'majors' folder.")
