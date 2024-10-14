import os
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Directory to save CSVs for courses and degree requirements
courses_output_dir = "majors_courses"
degree_requirements_output_dir = "degree_requirements"

for directory in [courses_output_dir, degree_requirements_output_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def remove_parentheses(text):
    """Remove any text within parentheses."""
    return re.sub(r'\s*\(.*?\)', '', text).strip()

def clean_text(text):
    """
    Clean text by removing non-breaking spaces and other encoding issues.
    """
    return text.replace('\xa0', ' ').replace('&nbsp;', ' ').replace('Â', '').strip()

def split_courses(text):
    """
    Split course entries separated by 'or' (case-insensitive).
    Returns a list of course strings.
    """
    # Use regex to split on ' or ', ' OR ', ' Or ', etc.
    return re.split(r'\s+[Oo][Rr]\s+', text)

def scrape_major_degree_requirements(driver, major_name, major_url):
    """Scrapes University Degree Requirements for a given major using Selenium."""
    # Clean the major_url by stripping leading/trailing spaces
    major_url = major_url.strip()
    # Build the full URL
    full_url = base_url + major_url

    print(f"Accessing {major_name} at {full_url}")

    # Navigate to the page with proper error handling and waiting
    try:
        driver.get(full_url)
        # Wait until the 'University Degree Requirements' section is present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'University Degree Requirements')]"))
        )
        time.sleep(2)  # Additional wait to ensure all dynamic content loads
    except Exception as e:
        print(f"Error loading page for {major_name} at {full_url}: {e}")
        return

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize an empty list to store degree requirements data
    degree_requirements = []

    # Find the 'University Degree Requirements' button
    requirements_button = soup.find('button', string=re.compile("University Degree Requirements", re.I))
    if not requirements_button:
        print(f"'University Degree Requirements' section not found for {major_name} at {full_url}")
        return

    # The toggle content is within the next sibling div with class 'toggle-content'
    toggle_parent = requirements_button.find_parent('h3')
    if not toggle_parent:
        print(f"Parent <h3> tag not found for 'University Degree Requirements' in {major_name} at {full_url}")
        return

    toggle_content = toggle_parent.find_next_sibling('div', class_='toggle-content')
    if not toggle_content:
        print(f"No toggle content found for 'University Degree Requirements' in {major_name} at {full_url}")
        return

    # Now, within toggle_content, find all sub-sections (toggle-wrap)
    sub_sections = toggle_content.find_all('div', class_='toggle-wrap')
    if not sub_sections:
        print(f"No sub-sections found in 'University Degree Requirements' for {major_name} at {full_url}")
        return

    for idx, sub_section in enumerate(sub_sections, start=1):
        # Each sub-section has a <h4> with a button for the category
        category_button = sub_section.find('button')
        if not category_button:
            print(f"No category button found in sub-section {idx} for {major_name}")
            continue

        category_name = clean_text(category_button.get_text())
        # The content is within the next sibling div with class 'toggle-content'
        category_content = sub_section.find('div', class_='toggle-content')
        if not category_content:
            print(f"No content found for category '{category_name}' in {major_name}")
            description = 'N/A'
        else:
            # Extract all text, preserving lists
            paragraphs = category_content.find_all(['p', 'li'])
            description_text = []
            for p in paragraphs:
                text = clean_text(p.get_text(separator=' ', strip=True))
                description_text.append(text)
            description = ' '.join(description_text) if description_text else 'N/A'

        # Append to the degree_requirements list
        degree_requirements.append({
            'Major': major_name,
            'Category': category_name,
            'Description': description,
            'URL': full_url
        })
        print(f"Added degree requirement: {category_name}")

    # Remove duplicate entries if any
    unique_degree_requirements = {tuple(req.items()) for req in degree_requirements}
    degree_requirements = [dict(t) for t in unique_degree_requirements]

    # Convert to DataFrame and save to CSV
    if degree_requirements:
        df = pd.DataFrame(degree_requirements, columns=['Major', 'Category', 'Description', 'URL'])
        # Clean the major name for filename
        csv_filename = remove_parentheses(major_name).replace(' ', '_').replace('/', '_') + ".csv"
        csv_file = os.path.join(degree_requirements_output_dir, csv_filename)
        df.to_csv(csv_file, index=False)
        print(f"Saved University Degree Requirements for {major_name} to {csv_file}")
    else:
        print(f"No degree requirements found for {major_name}")

def main_degree_requirements():
    # Configure Selenium to use headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize the WebDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Scrape degree requirements for each major
        for major_name, major_url in majors.items():
            print(f"\nScraping University Degree Requirements for {major_name}...")
            scrape_major_degree_requirements(driver, major_name, major_url)
            time.sleep(2)  # Delay to be respectful to the server
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main_degree_requirements()
