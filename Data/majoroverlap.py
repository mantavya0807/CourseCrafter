import pandas as pd
import os

# Folder path containing the original CSV files
folder_path = 'majors_courses_suryansh/'  # Replace with your folder path

# Folder path to save the cleaned files
cleaned_folder_path = 'majors/'  # New folder for cleaned files

# Create the new folder if it doesn't exist
if not os.path.exists(cleaned_folder_path):
    os.makedirs(cleaned_folder_path)

# Iterate over all files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is a CSV
    if file_name.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Load the CSV file
        majors_df = pd.read_csv(file_path)
        
        # Sort the dataframe by 'course_code' length in descending order to prioritize the longer ones
        majors_df.sort_values(by='course_code', key=lambda x: x.str.len(), ascending=False, inplace=True)

        # Initialize a list to store the final unique course codes
        final_unique_course_codes = []

        # Iterate through each course_code in the dataframe
        for course_code in majors_df['course_code']:
            # Split course codes by '|' to handle multiple codes in one cell
            parts = course_code.split('|')
            parts = [part.strip() for part in parts]  # Remove any extra spaces
            
            # Check if any part of the course code is already in the list of unique course codes
            if not any(existing_code in part or part in existing_code 
                       for existing_code in final_unique_course_codes 
                       for part in parts):
                final_unique_course_codes.append(course_code)

        # Create a cleaned dataframe with the filtered course codes
        majors_df_cleaned = majors_df[majors_df['course_code'].isin(final_unique_course_codes)]
        
        # Construct the output file path for the cleaned file in the new folder
        output_file_name = f'{file_name}'
        output_path = os.path.join(cleaned_folder_path, output_file_name)
        
        # Save the cleaned DataFrame to a new CSV file
        majors_df_cleaned.to_csv(output_path, index=False)
        
        # Print the output path of the cleaned file
        print(f"Cleaned file saved at: {output_path}")
