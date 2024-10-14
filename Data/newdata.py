import pandas as pd 

file_path= 'courses.csv'
df = pd.read_csv(file_path)

# Extract concurrent and prerequisite courses
df['concurrent'] = df['other'].str.extract(r'Concurrent:\s*([^;]+)')
df['prerequisite'] = df['other'].str.extract(r'Prerequisite(?: at Enrollment)?:\s*([^;]+)')


df.drop(columns=['other'], inplace=True)

# Display the modified DataFrame
print(df.head())

# Save the modified DataFrame to a new CSV file
df.to_csv('modify_courses.csv', index=False)
