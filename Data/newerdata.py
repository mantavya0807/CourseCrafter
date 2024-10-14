import pandas as pd 

# Load the CSV file
file_path = 'modify_courses.csv'
df = pd.read_csv(file_path)

# Extract semester standing requirements from the 'prerequisite' column
df['semester standing'] = df['prerequisite'].str.extract(r'(\d+th|\w+)-semester standing')

# Display the modified DataFrame
print(df.head())

# Save the modified DataFrame to a new CSV file
df.to_csv('newcourses.csv', index=False)