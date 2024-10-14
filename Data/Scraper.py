import requests
from bs4 import BeautifulSoup
import pandas as pd
import re  # Import regular expressions

# The URL of the Penn State undergraduate programs page
url = 'https://bulletins.psu.edu/programs/#filter=.filter_22'  # Adjust to the correct URL

# Send a GET request to fetch the page content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Lists to store data for majors, minors, and certificates
majors_data = []
minors_data = []
certificates_data = []

# Function to remove text within parentheses
def remove_parentheses(text):
    return re.sub(r'\s*\(.*?\)', '', text).strip()

# Find all the relevant program containers
programs = soup.find_all('li', class_='item')

# Loop through each program and extract necessary information
for program in programs:
    # Extract the full title and degree type
    title_element = program.find('span', class_='title')
    major_name_full = title_element.text.strip() if title_element else "Unknown"

    # Extract degree type (e.g., B.A., B.S.)
    degree_type = None
    if 'B.A.' in major_name_full:
        degree_type = 'B.A.'
        major_name = major_name_full.replace(', B.A.', '').strip()
    elif 'B.S.' in major_name_full:
        degree_type = 'B.S.'
        major_name = major_name_full.replace(', B.S.', '').strip()
    elif 'Minor' in major_name_full:
        degree_type = 'Minor'
        major_name = major_name_full.replace(', Minor', '').strip()
    elif 'Certificate' in major_name_full:
        degree_type = 'Certificate'
        major_name = major_name_full.replace(', Certificate', '').strip()
    
    # Remove text inside parentheses from the major name
    major_name = remove_parentheses(major_name)
    
    # Extract the college name
    keywords = program.find_all('span', class_='keyword')
    college_name = None
    for keyword in keywords:
        if 'College' in keyword.text:  # Checking if the keyword contains 'College'
            college_name = keyword.text.strip()
            break
    
    # Check if the program is available at University Park
    if 'University Park' in program.text:
        if degree_type == 'B.A.' or degree_type == 'B.S.':
            majors_data.append([major_name, degree_type, college_name])
        elif degree_type == 'Minor':
            minors_data.append([major_name, degree_type, college_name])
        elif degree_type == 'Certificate':
            certificates_data.append([major_name, degree_type, college_name])

# Convert the lists into pandas DataFrames
majors_df = pd.DataFrame(majors_data, columns=['Major', 'Degree Type', 'College'])
minors_df = pd.DataFrame(minors_data, columns=['Minor', 'Degree Type', 'College'])
certificates_df = pd.DataFrame(certificates_data, columns=['Certificate', 'Degree Type', 'College'])

# Save the data into separate CSV files
majors_df.to_csv('university_park_majors.csv', index=False)
minors_df.to_csv('university_park_minors.csv', index=False)
certificates_df.to_csv('university_park_certificates.csv', index=False)

print('Scraping complete. Data saved to university_park_majors.csv, university_park_minors.csv, and university_park_certificates.csv.')
