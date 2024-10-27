import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re

# Base URL for Penn State majors
base_url = 'https://bulletins.psu.edu/undergraduate/colleges/'

# Dictionary of majors and their corresponding URLs
majors = {
   "Accounting B.S.": "smeal-business/accounting-bs/",
   "Actuarial Science B.S.": "smeal-business/actuarial-science-bs/",
   "Advertising/Public Relations B.A.": "bellisario-communications/advertising-public-relations-ba/",
   "Aerospace Engineering B.S.": "engineering/aerospace-engineering-bs/",
   "African American Studies B.A.": "liberal-arts/african-african-american-studies-ba/",
   "African and African American Studies B.A.": "liberal-arts/african-african-american-studies-ba/",
   "African and African American Studies B.S.": "liberal-arts/african-african-american-studies-bs/",
   "African Studies B.A.": "liberal-arts/african-studies-ba/",
   "Agribusiness Management B.S.": "agricultural-sciences/agribusiness-management-bs/",
   "Agricultural and Biorenewable Systems Management B.S.": "agricultural-sciences/agricultural-biorenewable-systems-management-bs/",
   "Agricultural and Extension Education B.S.": "agricultural-sciences/agricultural-extension-education-bs/",
   "Agricultural Science B.S.": "agricultural-sciences/agricultural-science-bs/",
   "Animal Science B.S.": "agricultural-sciences/animal-science-bs/",
   "Anthropological Science B.S.": "liberal-arts/anthropological-science-bs/",
   "Anthropology B.A.": "liberal-arts/anthropology-ba/",
   "Architectural Engineering B.A.": "engineering/architectural-engineering-bae/",
   "Architecture B.S.": "arts-architecture/architecture-bs/",
   "Art Education B.S.": "arts-architecture/art-education-bs/",
   "Art History B.A.": "arts-architecture/art-history-ba/",
   "Art B.A.": "arts-architecture/art-ba/",
   "Asian Studies B.A.": "liberal-arts/asian-studies-ba/",
   "Astronomy and Astrophysics B.S.": "eberly-science/astronomy-astrophysics-bs/",
   "Biobehavioral Health B.S.": "health-human-development/biobehavioral-health-bs/",
   "Biochemistry and Molecular Biology B.S.": "biochemistry-molecular-biology-bs/",
   "Biological Engineering B.S.": "engineering/biological-engineering-bs/",
   "Biology B.S.": "eberly-science/biology-bs/",
   "Biomedical Engineering B.S.": "engineering/biomedical-engineering-bs/",
   "Biotechnology B.S.": "eberly-science/biotechnology-bs/",
   "Chemical Engineering B.S.": "engineering/chemical-engineering-bs/",
   "Chemistry B.S.": "eberly-science/chemistry-bs/",
   "Chinese B.A.": "liberal-arts/chinese-ba/",
   "Civil Engineering B.S.": "engineering/civil-engineering-bs/",
   "Classics and Ancient Mediterranean Studies B.A.": "liberal-arts/classics-ancient-mediterranean-studies-ba/",
   "Communication Arts and Sciences B.A.": "liberal-arts/communication-arts-sciences-ba/",
   "Communication Arts and Sciences B.S.": "liberal-arts/communication-arts-sciences-bs/",
   "Communication Sciences and Disorders B.S.": "health-human-development/communication-sciences-disorders-bs/",
   "Community, Environment, and Development B.S.": "agricultural-sciences/community-environment-development-bs/",
   "Comparative Literature B.A.": "comparative-literature-ba/",
   "Computer Engineering B.S.": "engineering/computer-engineering-bs/",
   "Computer Science B.S.": "engineering/computer-science-bs/",
   "Corporate Innovation and Entrepreneurship B.S.": "smeal-business/corporate-innovation-entrepreneurship-bs/",
   "Criminology B.A.": "liberal-arts/criminology-ba/",
   "Criminology B.S.": "liberal-arts/criminology-bs/",
   "Cybersecurity Analytics and Operations B.S.": "information-sciences-technology/cybersecurity-analytics-operations-bs/",
   "Data Sciences B.S.": "information-sciences-technology/data-sciences-bs/",
   "Earth Science and Policy B.S.": "earth-mineral-sciences/earth-science-policy-bs/",
   "Earth Sciences B.S.": "earth-mineral-sciences/earth-sciences-bs/",
   "Economics B.A.": "liberal-arts/economics-ba/",
   "Economics B.S.": "liberal-arts/economics-bs/",
   "Education and Public Policy B.S.": "education/education-public-policy-bs/",
   "Electrical Engineering B.S.": "engineering/electrical-engineering-bs/",
   "Elementary and Early Childhood Education B.S.":"elementary-early-childhood-education-bs/",
   "Elementary and Kindergarten Education B.S.": "education/elementary-kindergarten-education-bs/",
   "Energy Business and Finance B.S.": "earth-mineral-sciences/energy-business-finance-bs/",
   "Energy Engineering B.S.": "earth-mineral-sciences/energy-engineering-bs/",
   "Engineering Science B.S.": "engineering/engineering-science-bs/",
   "English B.A.": "liberal-arts/english-ba/",
   "Enterprise Technology Integration B.S.": "information-sciences-technology/enterprise-technology-integration-bs/",
   "Environmental Resource Management B.S.": "agricultural-sciences/environmental-resource-management-bs/",
   "Environmental Systems Engineering B.S.": "environmental-systems-engineering-bs/",
   "Film Production B.A.": "bellisario-communications/film-production-ba/",
   "Finance B.S.": "smeal-business/finance-bs/",
   "Food Science B.S.":  "agricultural-sciences/food-science-bs/",
   "Forestry B.S.": "agricultural-sciences/forest-ecosystem-management-bs/",
   "French B.A.": "liberal-arts/french-francophone-studies-ba/",
   "General Science B.S.": "eberly-science/integrative-science-bs/",
   "Geography B.A.": "earth-mineral-sciences/geography-ba/",
   "Geography B.S.": "earth-mineral-sciences/geography-bs/",
   "Geosciences B.S.": "earth-mineral-sciences/geosciences-bs/",
   "German B.A.": "liberal-arts/german-ba/",
   "Global and International Studies B.A.": "liberal-arts/global-international-studies-ba/",
   "Graphic Design B.A.": "arts-architecture/graphic-design-bdes/",
   "History B.A.": "liberal-arts/history-ba/",
   "Hospitality Management B.S.": "health-human-development/hospitality-management-bs/",
   "Human Development and Family Studies B.S.": "health-human-development/human-development-family-studies-bs/",
   "Information Sciences and Technology B.S.": "information-sciences-technology/information-sciences-technology-bs/",
   "International Politics B.A.": "liberal-arts/international-politics-ba/",
   "Italian B.A.": "liberal-arts/italian-ba/",
   "Italian B.S.": "liberal-arts/italian-bs/",
   "Japanese B.A.": "liberal-arts/japanese-ba/",
   "Jewish Studies B.A.": "liberal-arts/jewish-studies-ba/",
   "Journalism B.A.": "bellisario-communications/journalism-ba/",
   "Kinesiology B.S.": "health-human-development/kinesiology-bs/",
   "Korean B.A.": "liberal-arts/korean-ba/",
   "Labor and Human Resources B.A.": "liberal-arts/labor-human-resources-ba/",
   "Labor and Human Resources B.S.": "liberal-arts/labor-human-resources-bs/",
   "Landscape Contracting B.S.": "agricultural-sciences/landscape-contracting-bs/",
   "Latin American Studies B.A.": "liberal-arts/latin-american-studies-ba/",
   "Linguistics B.A.": "liberal-arts/linguistics-ba/",
   "Management Information Systems B.S.": "smeal-business/management-information-systems-bs/",
   "Management B.S.": "smeal-business/management-bs/",
   "Marketing B.S.": "smeal-business/marketing-bs/",
   "Materials Science and Engineering B.S.": "earth-mineral-sciences/materials-science-engineering-bs/",
   "Mathematics B.A.": "eberly-science/mathematics-ba/",
   "Mathematics B.S.": "eberly-science/mathematics-bs/",
   "Mechanical Engineering B.S.": "engineering/mechanical-engineering-bs/",
   "Media Studies B.A.": "bellisario-communications/media-studies-ba/",
   "Medieval Studies B.A.": "liberal-arts/medieval-studies-ba/",
   "Meteorology and Atmospheric Science B.S.": "earth-mineral-sciences/meteorology-atmospheric-science-bs/",
   "Microbiology B.S.": "eberly-science/microbiology-bs/",
   "Middle East Studies B.A.": "liberal-arts/middle-east-studies-ba/",
   "Middle Level Education B.S.": "education/middle-level-education-bs/",
   "Mining Engineering B.S.": "earth-mineral-sciences/mining-engineering-bs/",
   "Multidisciplinary Studies B.A.": "liberal-arts/multidisciplinary-studies-ba/",
   "Music B.A.": "arts-architecture/music-ba/",
   "Nuclear Engineering B.S.": "engineering/nuclear-engineering-bs/",
   "Nursing B.S.": "nursing/nursing-bsn/",
   "Nutritional Sciences B.S.": "health-human-development/nutritional-sciences-bs/",
   "Organizational Leadership B.A.": "liberal-arts/organizational-leadership-ba/",
   "Organizational Leadership B.S.": "liberal-arts/organizational-leadership-bs/",
   "Petroleum and Natural Gas Engineering B.S.": "earth-mineral-sciences/petroleum-natural-gas-engineering-bs/",
   "Pharmacology and Toxicology B.S.": "agricultural-sciences/pharmacology-toxicology-bs/",
   "Philosophy B.A.": "liberal-arts/philosophy-ba/",
   "Philosophy B.S.": "liberal-arts/philosophy-bs/",
   "Physics B.S.": "eberly-science/physics-bs/",
   "Planetary Science and Astronomy B.S.": "eberly-science/planetary-science-and-astronomy-bs/",
   "Plant Sciences B.S.": "agricultural-sciences/plant-sciences-bs/",
   "Political Science B.A.": "liberal-arts/political-science-ba/",
   "Political Science B.S.": "liberal-arts/political-science-bs/",
   "Premedical-Medical B.S.": "eberly-science/premedical-medical-bs/",
   "Premedicine B.S.": "eberly-science/premedicine-bs/",
   "Psychology B.A.": "liberal-arts/psychology-ba/",
   "Psychology B.S.": "liberal-arts/psychology-bs/",
   "Real Estate B.S.": "smeal-business/real-estate-bs/",
   "Recreation, Park, and Tourism Management B.S.": "health-human-development/recreation-park-tourism-management-bs/",
   "Rehabilitation and Human Services B.S.": "education/rehabilitation-human-services-bs/",
   "Risk Management B.S.": "smeal-business/risk-management-bs/",
   "Russian B.A.": "liberal-arts/russian-ba/",
   "Secondary Education B.S.": "education/secondary-education-bs/",
   "Security and Risk Analysis B.S.": "information-sciences-technology/security-risk-analysis-bs/",
   "Social Data Analytics B.S.": "liberal-arts/social-data-analytics-bs/",
   "Sociology B.A.": "liberal-arts/sociology-ba/",
   "Sociology B.S.": "liberal-arts/sociology-bs/",
   "Spanish B.A.": "liberal-arts/spanish-ba/",
   "Spanish B.S.": "liberal-arts/spanish-bs/",
   "Special Education B.S.": "education/special-education-bs/",
   "Statistics B.S.": "eberly-science/statistics-bs/",
   "Supply Chain and Information Systems B.S.": "smeal-business/supply-chain-information-systems-bs/",
   "Telecommunications and Media Industries B.A.": "telecommunications-media-industries-ba/",
   "Theatre B.A.": "arts-architecture/theatre-ba/",
   "Turfgrass Science B.S.": "agricultural-sciences/turfgrass-science-bs/",
   "Veterinary and Biomedical Sciences B.S.": "agricultural-sciences/veterinary-biomedical-sciences-bs/",
   "Wildlife and Fisheries Science B.S.": "agricultural-sciences/wildlife-fisheries-science-bs/",
   "Women's Studies B.A.": "liberal-arts/womens-studies-ba/",
   "Women's Studies B.S.": "liberal-arts/womens-studies-bs/",
   "Workforce Education and Development B.S.": "education/workforce-education-development-bs/",
   "World Language Education B.S.": "education/world-languages-k-12-education-bs/"
   # Add more majors here following the same pattern
}

output_folder = "Majors_Course_Plans"
os.makedirs(output_folder, exist_ok=True)

# Function to clean up file names
def clean_file_name(name):
    return re.sub(r'[^\w\s]', '', name).replace(" ", "_")

# Iterate over each major in the dictionary
for major, path in majors.items():
    # Create the full URL for each major
    url = base_url + path

    # Send a request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table
    table = soup.find('table', {'class': 'sc_plangrid'})

    # Initialize lists to store data
    data = {'Year': [], 'Semester': [], 'Course': [], 'Credits': []}

    # Check if the table exists
    if table:
        # Extract course information from the table
        year = None
        semester = None
        for row in table.find_all('tr'):
            # Identify year rows
            if 'plangridyear' in row.get('class', []):
                year = row.text.strip()
            # Identify semester rows
            elif 'plangridterm' in row.get('class', []):
                semesters = row.find_all('th')
                semester = [semesters[0].text.strip(), semesters[2].text.strip()]
            # Extract course and credits
            elif 'plangridsum' not in row.get('class', []) and 'plangridtotal' not in row.get('class', []):
                columns = row.find_all('td')
                # Left column (first semester)
                if len(columns) >= 4:
                    data['Year'].append(year)
                    data['Semester'].append(semester[0])
                    data['Course'].append(columns[0].text.strip())
                    data['Credits'].append(columns[1].text.strip())
                    # Right column (second semester)
                    data['Year'].append(year)
                    data['Semester'].append(semester[1])
                    data['Course'].append(columns[2].text.strip())
                    data['Credits'].append(columns[3].text.strip())

        # Convert data to a DataFrame
        df = pd.DataFrame(data)

        # Clean file name to avoid issues
        file_name = clean_file_name(major) + "_course_plan.csv"
        file_path = os.path.join(output_folder, file_name)

        # Save the DataFrame to a CSV file in the single folder
        df.to_csv(file_path, index=False)

        print(f'Saved {major} course plan to {file_path}')
    else:
        print(f'No course plan found for {major}.')