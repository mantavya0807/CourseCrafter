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
import logging

# Configure logging
logging.basicConfig(
    filename='scraper_minors.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Base URL for Penn State minors
base_url = 'https://bulletins.psu.edu/undergraduate/colleges/'

# Dictionary of minors and their corresponding URLs
minors = {
    "Accounting Minor": "smeal-business/accounting-minor/",
    "Computer Science Minor": "engineering/computer-science-minor/",
    "Psychology Minor": "liberal-arts/psychology-minor/",
    "Addictions and Recovery Minor":"education/addictions-recovery-minor/",
    "African American Studies Minor": "liberal-arts/african-american-studies-minor/",
    "African Studies":"liberal-arts/african-studies-minor/",
    "Agribusiness Management Minor": "agricultural-sciences/agribusiness-management-minor/",
    "Agricultural Systems Management Minor": "agricultural-sciences/agricultural-systems-management-minor/",
    "Arabic Language Minor": "liberal-arts/arabic-language-minor/",
    " Arboriculture Minor" : "agricultural-sciences/arboriculture-minor/",
    "Architectural History Minor": "arts-architecture/architectural-history-minor/",
    "Architecture Studies Minor" : "arts-architecture/architecture-studies-minor/",
    "Art History Minor": "arts-architecture/art-history-minor/",
    "Art Minor": "arts-architecture/art-minor/",
    "Asian Studies Minor": "liberal-arts/asian-studies-minor/",
    "Astrobiology Minor": "intercollege/astrobiology-minor/",
    "Astronomy and Astrophysics Minor": "eberly-science/astronomy-astrophysics-minor/",
    "Biochemistry and Molecular Biology Minor": "eberly-science/biochemistry-molecular-biology-minor/",
    "Bioethics and Medical Humanities Minor":"intercollege/bioethics-medical-humanities-minor/",
    "Biological Engineering Minor":"engineering/biological-engineering-minor/",
    "Biology Minor":"eberly-science/biology-minor/",
    "Biomedical Engineering, Minor":"engineering/biomedical-engineering-minor/",
    "Black Diaspora Studies Minor":"liberal-arts/black-diaspora-studies-minor/",
    "Business and the Liberal Arts Minor": "liberal-arts/business-liberal-arts-minor/",
    "Chemistry Minor": "eberly-science/chemistry-minor/",
    "Child Maltreatment and Advocacy Studies Minor":"child-maltreatment-advocacy-studies-minor/",
    "Chinese Language Minor": "liberal-arts/chinese-language-minor/",
    "Civic and Community Engagement Minor":"intercollege/civic-community-engagement-minor/",
    "Classics and Ancient Mediterranean Studies Minor": "liberal-arts/classics-ancient-mediterranean-studies-minor/",
    "Climatology Minor": "earth-mineral-sciences/climatology-minor/",
    "Communication and Social Justice Minor": "ellisario-communications/communication-social-justice-minor/",
    "Communication Arts and Sciences, Minor": "liberal-arts/communication-arts-sciences-minor/",
    "Computational Sciences Minor": "engineering/computational-sciences-minor/",
    "Computer Engineering, Minor (Engineering)": "engineering/computer-engineering-minor/",
    "Creative Writing Minor": "liberal-arts/creative-writing-minor/",
    "Cybersecurity Computational Foundations Minor": "engineering/cybersecurity-computational-foundations-minor/",
    "Digital Humanities Minor": "liberal-arts/digital-humanities-minor/",
    "Digital Media Trends and Analytics Minor": "bellisario-communications/digital-media-trends-analytics-minor/",
    "Disability Studies Minor":"intercollege/disability-studies-minor/",
    "Dispute Management and Resolution Minor":"liberal-arts/dispute-management-resolution-minor/",
    "Diversity and Inclusion in Health and Human Development Minor": "health-human-development/diversity-inclusion-health-human-development/",
    "Early Development and Education Minor": "education/early-development-education-minor/",
    "Earth and Sustainability Minor": "earth-mineral-sciences/earth-sustainability-minor/",
    "Earth Systems Minor": "earth-mineral-sciences/earth-systems-minor/",
    "East European Studies Minor": "liberal-arts/east-european-studies-minor/",
    "Economics Minor": "liberal-arts/economics-minor/",
    "Education and Public Policy Minor":"education/education-public-policy-minor/",
    "Electrochemical Engineering Minor": "earth-mineral-sciences/electrochemical-engineering-minor/",
    "Energy Business and Finance, Minor": "earth-mineral-sciences/energy-business-finance-minor/",
    "Energy Engineering Minor": "earth-mineral-sciences/energy-engineering-minor/",
    "Engineering Design Minor": "engineering/engineering-design-minor/",
    "Engineering Leadership Development Minor":"engineering/engineering-leadership-development-minor/",
    "Engineering Mechanics Minor": "engineering/engineering-mechanics-minor/",
    "English Minor (Liberal Arts)": "liberal-arts/english-minor/",
    "Entomology Minor": "agricultural-sciences/entomology-minor/",
    "Entrepreneurship and Innovation Minor": "intercollege/entrepreneurship-innovation-minor/",
    "Environmental and Renewable Resource Economics Minor": "agricultural-sciences/environmental-renewable-resource-economics-minor/",
    "Environmental Engineering Minor": "engineering/environmental-engineering-minor/",
    "Environmental Inquiry Minor": "intercollege/environmental-inquiry-minor/",
    "Environmental Resource Management Minor":"agricultural-sciences/environmental-resource-management-minor/",
    "Environmental Soil Science Minor": "agricultural-sciences/environmental-soil-science-minor/",
    "Environmental Systems Engineering Minor": "earth-mineral-sciences/environmental-systems-engineering-minor/",
    "Equine Science Minor": "agricultural-sciences/equine-science-minor/",
    "Ethics Minor":"liberal-arts/ethics-minor/",
    "Film Studies Minor": "bellisario-communications/film-studies-minor/",
    "Food Systems Minor": "agricultural-sciences/food-systems-minor/",
    "Forest Ecosystems Minor": "agricultural-sciences/forest-ecosystems-minor/",
    "French and Francophone Studies Minor": "liberal-arts/french-francophone-studies-minor/",
    "Geographic Information Science Minor": "earth-mineral-sciences/geographic-information-science-minor/",
    "Geography Minor": "earth-mineral-sciences/geography-minor/",
    "Geophysics Minor": "earth-mineral-sciences/geophysics-minor/",
    "Geosciences, Minor": "earth-mineral-sciences/geosciences-minor/",
    "German Minor": "liberal-arts/german-minor/",
    "Global and International Studies Minor": "liberal-arts/global-international-studies-minor/",
    "Global Health Minor": "health-human-development/global-health-minor/",
    "Global Security Minor": "liberal-arts/global-security-minor/",
    "Graphic Design Minor": "arts-architecture/graphic-design-minor/",
    "Health Policy and Administration Minor": "health-human-development/health-policy-administration-minor/",
    "Hebrew Minor": "liberal-arts/hebrew-minor/",
    "Horticulture Minor": "agricultural-sciences/horticulture-minor/",
    "Human Development and Family Studies Minor": "health-human-development/human-development-family-studies-minor/",
    "Information Sciences and Technology for Aerospace Engineering Minor": "engineering/information-sciences-technology-aerospace-engineering-minor/",
    "Information Sciences and Technology for Earth and Mineral Sciences Minor": "earth-mineral-sciences/information-sciences-technology-earth-mineral-sciences-minor/",
    "Information Sciences and Technology for Industrial Engineering Minor": "engineering/information-sciences-technology-industrial-engineering-minor/",
    "Information Sciences and Technology for Labor Studies and Employment Relations Minor": "liberal-arts/information-sciences-technology-labor-studies-employment-relations-minor/",
    "Information Sciences and Technology for Mathematics Minor": "eberly-science/information-sciences-technology-mathematics-minor/",
    "Information Sciences and Technology for Telecommunications Minor": "bellisario-communications/information-sciences-technology-telecommunications-minor/",
    "Information Sciences and Technology in Communication Arts and Sciences and Labor and Employment Relations Minor": "liberal-arts/information-sciences-technology-communications-arts-sciences-labor-employment-relations-minor/",
    "Information Sciences and Technology in Health Policy and Administration Minor": "health-human-development/information-sciences-technology-health-policy-administration-minor/",
    "Information Sciences and Technology Minor": "information-sciences-technology/information-sciences-technology-minor/",
    "Information Systems Management Minor": "smeal-business/information-systems-management-minor/",
    "International Agriculture Minor": "agricultural-sciences/international-agriculture-minor/",
    "International Arts Minor": "arts-architecture/international-arts-minor/",
    "International Business Minor": "smeal-business/international-business-minor/",
    "International Engineering Minor": "engineering/international-engineering-minor/",
    "Italian Minor": "liberal-arts/italian-minor/",
    "Japanese Language Minor": "liberal-arts/japanese-language-minor/",
    "Jazz Performance Minor": "arts-architecture/jazz-performance-minor/",
    "Jewish Studies Minor": "liberal-arts/jewish-studies-minor/",
    "Journalism Minor": "bellisario-communications/journalism-minor/",
    "Kinesiology Minor": "health-human-development/kinesiology-minor/",
    "Korean Language Minor": "liberal-arts/korean-language-minor/",
    "Labor and Human Resources Minor": "liberal-arts/labor-human-resources-minor/",
    "Landscape Architecture Minor": "arts-architecture/landscape-architecture-minor/",
    "Latin American Studies Minor": "liberal-arts/latin-american-studies-minor/",
    "Latin Minor": "liberal-arts/latin-minor/",
    "Latina and Latino Studies Minor": "liberal-arts/latina-latino-studies-minor/",
    "Leadership Development Minor": "agricultural-sciences/leadership-development-minor/",
    "Legal Environment of Business Minor": "smeal-business/legal-environment-business-minor/",
    "Legal Studies Minor": "liberal-arts/legal-studies-minor/",
    "Linguistics Minor": "liberal-arts/linguistics-minor/",
    "Longevity, Aging and Generational Studies Minor": "intercollege/longevity-aging-generational-studies-minor/",
    "Marine Sciences Minor": "eberly-science/marine-sciences-minor/",
    "Mathematics Minor (Science)": "eberly-science/mathematics-minor/",
    "Media Studies Minor": "bellisario-communications/media-studies-minor/",
    "Medieval Studies Minor": "liberal-arts/medieval-studies-minor/",
    "Meteorology Minor": "earth-mineral-sciences/meteorology-minor/",
    "Microbiology Minor": "eberly-science/microbiology-minor/",
    "Middle East Studies Minor": "liberal-arts/middle-east-studies-minor/",
    "Military Studies Minor": "intercollege/military-studies-minor/",
    "Mining Engineering Minor":"earth-mineral-sciences/mining-engineering-minor/",
    "Mushroom Science and Technology Minor": "agricultural-sciences/mushroom-science-technology-minor/",
    "Music Performance Minor": "arts-architecture/music-performance-minor/",
    "Music Studies Minor": "arts-architecture/music-studies-minor/",
    "Music Technology Minor": "arts-architecture/music-technology-minor/",
    "Nanotechnology Minor": "engineering/nanotechnology-minor/",
    "Natural Science Minor": "eberly-science/natural-science-minor/",
    "Neuroscience Minor": "intercollege/neuroscience-minor/",
    "Nutrition Studies Minor": "health-human-development/nutrition-studies-minor/",
    "Nutritional Sciences Minor": "health-human-development/nutritional-sciences-minor/",
    "Off-Road Equipment, Minor": "agricultural-sciences/off-road-equipment-minor/",
    "One Health Minor":"agricultural-sciences/one-health-minor/",
    "Organizational Leadership, Minor": "liberal-arts/organizational-leadership-minor/",
    "Pennsylvania Studies Minor": "liberal-arts/pennsylvania-studies-minor/",
    "Petroleum and Natural Gas Engineering Minor": "earth-mineral-sciences/petroleum-natural-gas-engineering-minor/",
    "Philosophy Minor": "liberal-arts/philosophy-minor/",
    "Photography Minor": "arts-architecture/photography-minor/",
    "Physics Minor": "eberly-science/physics-minor/",
    "Planetary Science and Astronomy Minor": "eberly-science/planetary-science-astronomy-minor/",
    "Plant Pathology Minor": "agricultural-sciences/plant-pathology-minor/",
    "Political Science Minor": "liberal-arts/political-science-minor/",
    "Politics and Public Policy Minor": "liberal-arts/politics-public-policy-minor/",
    "Polymer Science, Minor": "earth-mineral-sciences/polymer-science-minor/",
    "Portuguese Minor": "liberal-arts/portuguese-minor/",
    "Poultry and Avian Science Minor": "agricultural-sciences/poultry-avian-science-minor/",
    "Psychology Minor": "liberal-arts/psychology-minor/",
    "Public Policy and Leadership Across Sectors Minor": "liberal-arts/public-policy-leadership-across-sectors-minor/",
    "Recreation, Park, and Tourism Management Minor": "health-human-development/recreation-park-tourism-management-minor/",
    "Rehabilitation and Human Services Minor": "education/rehabilitation-human-services-minor/",
    "Religious Studies Minor": "liberal-arts/religious-studies-minor/",
    "Residential Construction Minor": "engineering/residential-construction-minor/",
    "Rhetoric Minor": "liberal-arts/rhetoric-minor/",
    "Russian Minor": "liberal-arts/russian-minor/",
    "Science, Technology, and Society, Minor":"intercollege/science-technology-society-minor/",
    "Security and Risk Analysis Minor": "information-sciences-technology/security-risk-analysis-minor/",
    "Service Enterprise Engineering Minor": "engineering/service-enterprise-engineering-minor/",
    "Sexuality and Gender Studies Minor": "liberal-arts/sexuality-gender-studies-minor/",
    "Six Sigma Minor": "engineering/six-sigma-minor/",
    "Social Justice in Education Minor": "education/social-justice-education-minor/",
    "Sociology Minor": "liberal-arts/sociology-minor/",
    "Spanish Minor": "liberal-arts/spanish-minor/",
    "Special Education Minor": "education/special-education-minor/",
    "Sport Studies Minor": "health-human-development/sport-studies-minor/",
    "Statistics Minor (Science)": "eberly-science/statistics-minor/",
    "Supply Chain and Information Sciences and Technology Minor": "smeal-business/supply-chain-information-sciences-technology-minor/",
    "Sustainability Leadership Minor": "intercollege/sustainability-leadership-minor/",
    "Teaching English to Speakers of Other Languages Minor": "liberal-arts/teaching-english-speakers-other-languages-minor/",
    "Technical Writing Minor": "liberal-arts/technical-writing-minor/",
    "Theatre Minor": "arts-architecture/theatre-minor/",
    "Watersheds and Water Resources Minor": "earth-mineral-sciences/watersheds-water-resources-minor/",
    "Wildlife and Fisheries Science Minor": "agricultural-sciences/wildlife-fisheries-science-minor/",
    "Women's Studies Minor": "liberal-arts/womens-studies-minor/",
    "World Literature Minor": "liberal-arts/world-literature-minor/"  
}

# Directory to save CSVs for minors
output_dir = "minors_courses"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

def scrape_minor_courses(driver, minor_name, minor_url):
    """Scrapes program requirements and course data for a given minor using Selenium."""
    # Clean the minor_url by stripping leading/trailing spaces
    minor_url = minor_url.strip()
    # Build the full URL
    full_url = base_url + minor_url

    logging.info(f"Accessing {minor_name} at {full_url}")
    print(f"Accessing {minor_name} at {full_url}")

    # Navigate to the page with proper error handling and waiting
    try:
        driver.get(full_url)
        # Wait until the 'Program Requirements' section is present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "programrequirementstextcontainer"))
        )
        time.sleep(2)  # Additional wait to ensure all dynamic content loads
    except Exception as e:
        logging.error(f"Error loading page for {minor_name} at {full_url}: {e}")
        print(f"Error loading page for {minor_name} at {full_url}: {e}")
        return

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize variables to store program requirements and course data
    total_credits = None
    program_policies = []
    mandatory_courses = []
    selectable_groups = []
    current_select_group = None

    # ---------------------------
    # Extract Program Requirements
    # ---------------------------
    try:
        program_requirements_container = soup.find('div', id='programrequirementstextcontainer')
        if not program_requirements_container:
            logging.warning(f"'Program Requirements' container not found for {minor_name}")
            print(f"'Program Requirements' container not found for {minor_name}")
        else:
            # Extract total credits from the first table
            program_table = program_requirements_container.find('table', class_='tbl_programrequirements')
            if program_table:
                tbody = program_table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            requirement = clean_text(cols[0].get_text())
                            credits_text = clean_text(cols[1].get_text())
                            # Assuming the first requirement is 'Requirements for the Minor' with total credits
                            if requirement.lower() == 'requirements for the minor':
                                total_credits_match = re.search(r'(\d+)', credits_text)
                                if total_credits_match:
                                    total_credits = int(total_credits_match.group(1))
                                    logging.info(f"Total credits for {minor_name}: {total_credits}")
                                    print(f"Total credits for {minor_name}: {total_credits}")
            else:
                logging.warning(f"No 'tbl_programrequirements' table found for {minor_name}")
                print(f"No 'tbl_programrequirements' table found for {minor_name}")

            # Extract program policies from paragraphs
            policies = program_requirements_container.find_all('p')
            for policy in policies:
                policy_text = clean_text(policy.get_text())
                program_policies.append(policy_text)
                logging.info(f"Program policy for {minor_name}: {policy_text}")
                print(f"Program policy for {minor_name}: {policy_text}")
    except Exception as e:
        logging.error(f"Error extracting program requirements for {minor_name}: {e}")
        print(f"Error extracting program requirements for {minor_name}: {e}")

    # ---------------------------
    # Extract Course Listings
    # ---------------------------
    try:
        # Find the 'Requirements for the Minor' section
        requirements_header = program_requirements_container.find('h3', string=re.compile("Requirements for the Minor", re.I))
        if not requirements_header:
            logging.warning(f"'Requirements for the Minor' header not found for {minor_name}")
            print(f"'Requirements for the Minor' header not found for {minor_name}")
        else:
            # The course list table is after the header
            course_table = requirements_header.find_next('table', class_='sc_courselist')
            if not course_table:
                logging.warning(f"No 'sc_courselist' table found for {minor_name}")
                print(f"No 'sc_courselist' table found for {minor_name}")
            else:
                tbody = course_table.find('tbody')
                if not tbody:
                    logging.warning(f"No table body found in 'sc_courselist' for {minor_name}")
                    print(f"No table body found in 'sc_courselist' for {minor_name}")
                else:
                    rows = tbody.find_all('tr')
                    for idx, row in enumerate(rows, start=1):
                        row_classes = row.get('class', [])
                        # Debug: Print row number and classes
                        logging.info(f"Processing row {idx} with classes: {row_classes}")
                        print(f"Processing row {idx} with classes: {row_classes}")

                        # Skip header rows or area headers
                        if 'areaheader' in row_classes or 'areasubheader' in row_classes:
                            logging.info(f"Skipping header row {idx}")
                            print(f"Skipping header row {idx}")
                            continue

                        # Check if the row contains a 'Select X credits' directive
                        select_directive = row.find('span', string=re.compile(r'Select\s+\d+(-\d+)?\s+credits?', re.I))
                        if select_directive:
                            # Extract the number of credits to select
                            select_number_match = re.search(r'Select\s+(\d+)(?:-\d+)?\s+credits?', select_directive.text, re.I)
                            if select_number_match:
                                select_number = select_number_match.group(1)
                                # Extract the selection criteria text
                                selection_text = clean_text(select_directive.text)
                                current_select_group = {
                                    'Select_Number': select_number,
                                    'Description': selection_text,
                                    'Options': []
                                }
                                selectable_groups.append(current_select_group)
                                logging.info(f"Found selectable group: {selection_text}")
                                print(f"Found selectable group: {selection_text}")
                            continue  # Move to the next row

                        # Now, process course rows
                        # Check if the row is a selectable option (indented)
                        block_indent = row.find('div', class_='blockindent')
                        if block_indent:
                            # This is a selectable option
                            course_links = block_indent.find_all('a', class_='bubblelink code')
                            if not course_links:
                                # Sometimes, courses might not have links; attempt to extract text
                                course_code_text = block_indent.get_text(strip=True)
                                course_codes = split_courses(course_code_text)
                            else:
                                course_codes = [clean_text(link.get_text()) for link in course_links]

                            # Check if 'or' is present in the course title
                            title_td = row.find('td', class_='titlecol')
                            if title_td:
                                course_title_text = clean_text(title_td.get_text())
                                if re.search(r'\bor\b', course_title_text, re.I):
                                    # Combine course codes with '|'
                                    combined_course_codes = ' | '.join(course_codes)
                                    # Optionally, you can also combine titles or choose one
                                    # For simplicity, we'll keep the first title
                                    course_title = re.split(r'\bor\b', course_title_text, flags=re.I)[0].strip()
                                    combined_title = ' | '.join([clean_text(title_td.get_text())] * len(course_codes))
                                    # Alternatively, keep both titles
                                    # combined_title = ' | '.join(re.split(r'\bor\b', course_title_text, flags=re.I))
                                    # Here, we choose to keep the first part
                                    course_title = ' | '.join([c.replace('&nbsp;', ' ') for c in course_title_text.split('or')])
                                else:
                                    course_title = course_title_text
                            else:
                                course_title = 'N/A'

                            # Extract credits
                            credits_td = row.find('td', class_='hourscol')
                            credits = clean_text(credits_td.get_text()) if credits_td else 'N/A'

                            # Handle 'or' in course codes by combining them
                            if len(course_codes) > 1:
                                combined_course_codes = ' | '.join(course_codes)
                            else:
                                combined_course_codes = course_codes[0]

                            # Add to the current selectable group
                            if current_select_group:
                                selectable_groups[-1]['Options'].append({
                                    'Course_Code': combined_course_codes,
                                    'Course_Title': course_title,
                                    'Credits': credits
                                })
                                logging.info(f"Added selectable course: {combined_course_codes} - {course_title} ({credits} Credits)")
                                print(f"Added selectable course: {combined_course_codes} - {course_title} ({credits} Credits)")
                            else:
                                # Edge case: selectable option without a preceding select directive
                                logging.warning(f"Selectable course found without a selection group: {combined_course_codes} - {course_title}")
                                print(f"Selectable course found without a selection group: {combined_course_codes} - {course_title}")
                            continue  # Move to the next row

                        # Handle other rows that might describe selection criteria without specific courses
                        # For example: "Select 0-3 credits of BMB courses at the 400-level"
                        description_directive = row.find('span', class_='courselistcomment')
                        if description_directive and 'select' in description_directive.text.lower():
                            selection_text = clean_text(description_directive.text)
                            current_select_group = {
                                'Select_Number': '0-3',
                                'Description': selection_text,
                                'Options': []
                            }
                            selectable_groups.append(current_select_group)
                            logging.info(f"Found selectable group: {selection_text}")
                            print(f"Found selectable group: {selection_text}")
                            continue

                        # This is a mandatory course
                        logging.info(f"Handling mandatory course row {idx}")
                        print(f"Handling mandatory course row {idx}")
                        code_col = row.find('td', class_='codecol')
                        if not code_col:
                            logging.warning(f"Skipping row {idx} as 'codecol' not found.")
                            print(f"Skipping row {idx} as 'codecol' not found.")
                            continue

                        # Extract all course codes (links)
                        code_links = code_col.find_all('a', class_='bubblelink code')
                        if code_links:
                            course_codes = [clean_text(link.get_text()) for link in code_links]
                        else:
                            # Fallback to plain text if no links are found
                            code_text = clean_text(code_col.get_text())
                            course_codes = split_courses(code_text)

                        # Check if 'or' is present in the course title
                        if code_col.find('div', class_='blockindent'):
                            # Already handled above
                            continue

                        title_td = row.find('td', class_='titlecol')
                        if title_td:
                            course_title = clean_text(title_td.get_text())
                        else:
                            # Sometimes, the title might be embedded differently
                            # Attempt to extract from the second 'td' if available
                            all_tds = row.find_all('td')
                            if len(all_tds) >= 2:
                                course_title = clean_text(all_tds[1].get_text())
                            else:
                                course_title = 'N/A'

                        # Extract credits
                        credits_td = row.find('td', class_='hourscol')
                        if credits_td:
                            credits = clean_text(credits_td.get_text())
                        else:
                            # Attempt to extract from the third 'td' if available
                            all_tds = row.find_all('td')
                            if len(all_tds) >= 3:
                                credits = clean_text(all_tds[2].get_text())
                            else:
                                credits = 'N/A'

                        for code in course_codes:
                            mandatory_courses.append({
                                'Course_Code': code,
                                'Course_Title': course_title,
                                'Credits': credits
                            })
                            logging.info(f"Added mandatory course: {code} - {course_title} ({credits} Credits)")
                            print(f"Added mandatory course: {code} - {course_title} ({credits} Credits)")
    except Exception as e:
        logging.error(f"Error extracting course listings for {minor_name}: {e}")
        print(f"Error extracting course listings for {minor_name}: {e}")

    # ---------------------------
    # Prepare and Save Data
    # ---------------------------
    try:
        # Remove duplicate mandatory courses if any
        unique_mandatory = {tuple(course.items()) for course in mandatory_courses}
        mandatory_courses = [dict(t) for t in unique_mandatory]

        # Prepare the final course list
        final_courses = {
            'Mandatory Courses': mandatory_courses,
            'Selectable Groups': selectable_groups
        }

        # Convert to DataFrame and save to CSV
        # First, create a DataFrame for mandatory courses
        if final_courses['Mandatory Courses']:
            df_mandatory = pd.DataFrame(final_courses['Mandatory Courses'])
            df_mandatory['Type'] = 'Mandatory'
        else:
            df_mandatory = pd.DataFrame(columns=['Course_Code', 'Course_Title', 'Credits', 'Type'])

        # Next, create DataFrames for selectable groups
        selectable_data = []
        for group in final_courses['Selectable Groups']:
            select_num = group['Select_Number']
            description = group.get('Description', '')
            for option in group['Options']:
                selectable_data.append({
                    'Course_Code': option['Course_Code'],
                    'Course_Title': option['Course_Title'],
                    'Credits': option['Credits'],
                    'Type': f'Select {select_num} Credits'
                })
            # If no options, still record the selection criteria
            if not group['Options']:
                selectable_data.append({
                    'Course_Code': '',
                    'Course_Title': description,
                    'Credits': '',
                    'Type': f'Select {select_num} Credits'
                })
                logging.info(f"Added selectable group without specific courses: {description}")
                print(f"Added selectable group without specific courses: {description}")

        if selectable_data:
            df_selectable = pd.DataFrame(selectable_data)
        else:
            df_selectable = pd.DataFrame(columns=['Course_Code', 'Course_Title', 'Credits', 'Type'])

        # Combine mandatory and selectable DataFrames
        if not df_mandatory.empty and not df_selectable.empty:
            df_all = pd.concat([df_mandatory, df_selectable], ignore_index=True)
        elif not df_mandatory.empty:
            df_all = df_mandatory
        else:
            df_all = df_selectable

        # Add columns for Minor, Total Credits, Program Policies, and URL
        df_all['Minor'] = minor_name
        df_all['Total_Credits'] = total_credits if total_credits else 'N/A'
        df_all['Program_Policies'] = '; '.join(program_policies) if program_policies else 'N/A'
        df_all['URL'] = full_url

        # Reorder columns for better readability
        df_all = df_all[['Minor', 'Total_Credits', 'Course_Code', 'Course_Title', 'Credits', 'Type', 'Program_Policies', 'URL']]

        # Clean the minor name for filename
        csv_filename = remove_parentheses(minor_name).replace(' ', '_').replace('/', '_') + ".csv"
        csv_file = os.path.join(output_dir, csv_filename)
        df_all.to_csv(csv_file, index=False)
        logging.info(f"Saved {minor_name} courses and requirements to {csv_file}")
        print(f"Saved {minor_name} courses and requirements to {csv_file}")
    except Exception as e:
        logging.error(f"Error saving data for {minor_name}: {e}")
        print(f"Error saving data for {minor_name}: {e}")

def main():
    # Configure Selenium to use headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize the WebDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Scrape courses and program requirements for each minor
        for minor_name, minor_url in minors.items():
            print(f"\nScraping data for {minor_name}...")
            logging.info(f"Scraping data for {minor_name}")
            scrape_minor_courses(driver, minor_name, minor_url)
            time.sleep(2)  # Delay to be respectful to the server
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
