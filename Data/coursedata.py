import pandas as pd

# Load the CSV file
file_path = 'nlpplease.csv'
df = pd.read_csv(file_path)

# Function to split the concurrent and prerequisite columns by '&' and convert to lists
def split_to_list(column_value):
    if pd.isna(column_value):
        return []
    return [item.strip() for item in column_value.replace('&', ',').split(',')]

# Apply the function to 'concurrent' and 'prerequisite' columns
df['concurrent'] = df['concurrent'].apply(split_to_list)
df['prerequisite'] = df['prerequisite'].apply(split_to_list)

# Save the modified DataFrame back to CSV
output_file_path = 'nlppleasemodified.csv'
df.to_csv(output_file_path, index=False)

print("Transformation completed and saved to:", output_file_path)
