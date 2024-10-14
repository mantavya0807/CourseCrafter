import csv

# Define the path for the CSV file
path = './degree_requirements_ba.csv'

# Define the header and data to be written into the CSV file
headers = ['Category', 'Description', 'Credits']

data = [
    {
        'Category': 'World Language',
        'Description': 'Proficiency in a world language in addition to English. Demonstrated through coursework or examination.',
        'Credits': '0-12'
    },
    {
        'Category': 'B.A. Fields',
        'Description': 'Humanities, Social and Behavioral Sciences, Arts, World Languages, Natural Sciences, Quantification. Credits must be selected from the list of approved courses.',
        'Credits': '9'
    },
    {
        'Category': 'World Cultures',
        'Description': '3 credits from an approved list. Can count towards major, minor, or elective requirements.',
        'Credits': '0-3'
    },
    {
        'Category': 'Other University Requirements',
        'Description': 'First Year Engagement, Cultural Diversity, and Writing Across the Curriculum requirements.',
        'Credits': 'Varies'
    },
    {
        'Category': 'Total Minimum Credits',
        'Description': 'A minimum of 120 credits required for a baccalaureate degree.',
        'Credits': '120'
    },
    {
        'Category': 'Quality of Work',
        'Description': 'Candidates must maintain a minimum GPA of 2.0 to graduate.',
        'Credits': 'N/A'
    }
]

# Write to CSV file
with open(path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # Write header
    writer.writeheader()
    
    # Write data
    for record in data:
        writer.writerow(record)

print('CSV file created successfully!')



