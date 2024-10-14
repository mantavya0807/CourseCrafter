import pandas as pd
import re

# Load the CSV file
file_path = 'newcourses.csv'
df = pd.read_csv(file_path)

# Define function to move "concurrent" and everything after it to the concurrent column
def split_prerequisite_concurrent(prerequisite):
    if pd.isna(prerequisite):  # Check if the prerequisite is NaN
        return prerequisite, None
    
    # Look for the word "concurrent" and everything after it
    concurrent_match = re.search(r'\bConcurrent\b.*', prerequisite, re.IGNORECASE)
    
    if concurrent_match:
        concurrent_courses = concurrent_match.group(0).strip()
        # Remove the concurrent course from the prerequisite
        prerequisite = re.sub(r'\bConcurrent\b.*', '', prerequisite, flags=re.IGNORECASE).strip()
        return prerequisite, concurrent_courses
    
    return prerequisite, None

# Apply the function to split concurrent and prerequisite courses
df[['prerequisite', 'concurrent']] = df.apply(
    lambda row: pd.Series(split_prerequisite_concurrent(row['prerequisite'])), axis=1
)

# Save the modified DataFrame to a new CSV file
output_file_path = 'updatedcourses_with_concurrent.csv'
df.to_csv(output_file_path, index=False)

# Display the first few rows of the modified DataFrame
print(df.head())
