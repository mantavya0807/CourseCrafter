import pandas as pd
import re

# Load the CSV file
file_path = 'updatedcourses_with_concurrent.csv'
df = pd.read_csv(file_path)

# Define function to extract semester standing and remove it from the prerequisite
def extract_and_remove_semester_standing(prerequisite):
    if pd.isna(prerequisite):  # Check if the prerequisite is NaN
        return prerequisite, None
    written_number_to_digit = {
        "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
        "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10
    }
    
    for word, digit in written_number_to_digit.items():
        match = re.search(fr'\b{word}\b|\b{digit}(?:st|nd|rd|th)\b', prerequisite, re.IGNORECASE)
        if match:
            # If the phrase includes "or higher", append "+"
            if "or higher" in prerequisite.lower():
                semester_standing = f'{digit}+'
            else:
                semester_standing = digit
            
            # Remove the matched part from the prerequisite column
            updated_prerequisite = re.sub(fr'\b{word}\b|\b{digit}(?:st|nd|rd|th)\b(?:\s*or\s*higher)?', '', prerequisite, flags=re.IGNORECASE).strip()
            return updated_prerequisite, semester_standing
    
    return prerequisite, None

# Apply the function to both extract and remove semester standing
df[['prerequisite', 'semester standing']] = df.apply(
    lambda row: pd.Series(extract_and_remove_semester_standing(row['prerequisite'])), axis=1
)

# Define function to replace "and" with "&" and "or" with "|"
def replace_conjunctions(text):
    if pd.isna(text):  # Check if the text is NaN
        return text
    text = re.sub(r'\band\b', '&', text, flags=re.IGNORECASE)
    text = re.sub(r'\bor\b', '|', text, flags=re.IGNORECASE)
    return text

# Apply the conjunction replacements
df['prerequisite'] = df['prerequisite'].apply(replace_conjunctions)

# Replace the specific math phrase with the required transformation
def replace_math_prerequisite(text):
    if pd.isna(text):  # Check if the text is NaN
        return text
    text = re.sub(
        r'MATH\s*\d+\s*\|\s*a\s*higher\s*math\s*course\s*\|\s*a\s*satisfactory\s*score\s*on\s*the\s*mathematics\s*placement\s*examination', 
        r'MATH 21 / Math 21 +',
        text, flags=re.IGNORECASE
    )
    return text

# Apply the math phrase replacement
df['prerequisite'] = df['prerequisite'].apply(replace_math_prerequisite)

# Save the modified DataFrame to a new CSV file
df.to_csv('nlpplease.csv', index=False)

# Display the first few rows of the modified DataFrame
print(df.head())

