import pandas as pd

# List of specific substrings to remove from cells (not entire rows)
remove_strings = [
    '\xa0',  # Non-breaking space represented as \xa0
    'students must be participating in the pennypacker experience to take this course', 
    'prior approval by department',
    'prior approval of proposed assignment by instructor', 
    'one course in fluid mechanics'
]

def clean_csv(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Function to remove specific substrings from cells
    def remove_strings_in_row(text):
        # Iterate over each string in the remove_strings list
        for remove_string in remove_strings:
            # Replace the unwanted substring with an empty string
            text = text.replace(remove_string, '')  
        return text

    # Apply the function to every cell in the DataFrame
    cleaned_df = df.applymap(lambda x: remove_strings_in_row(str(x)))

    # Save the cleaned data back to the original CSV file
    cleaned_df.to_csv(csv_file, index=False)
    print(f"Cleaned CSV saved to {csv_file}")

# Clean the CSV file in place
input_file = 'courses.csv'

try:
    clean_csv(input_file)  # Perform the cleaning and overwrite the original file
except Exception as e:
    print(f"An error occurred while cleaning the CSV: {e}")
