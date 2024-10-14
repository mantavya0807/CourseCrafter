import pandas as pd

file_path = 'university_park_majors.csv'
majors_df = pd.read_csv(file_path)

# Remove duplicates based on the 'Major' column
majors_df_cleaned = majors_df.drop_duplicates(subset=['Major'], keep='first')

# Save the cleaned DataFrame to a new CSV file
output_path = 'university_park_majors_cleaned.csv'
majors_df_cleaned.to_csv(output_path, index=False)

output_path  # Display the path to the cleaned file