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
    filename='scraper_certificates.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Base URL for Penn State certificate programs
base_url = 'https://bulletins.psu.edu/undergraduate/colleges/'

# Dictionary of certificates and their corresponding URLs
certificates = {
    "Advanced Instructor Development for Professionals": "education/advanced-instructor-development-professionals-certificate/",
    "Africa-Asia Studies": "liberal-arts/africa-asia-studies-certificate/",
    "African Literature, Visual Arts, and Performance": "liberal-arts/african-literature-visual-arts-performance-certificate/",
    "Agricultural Stewardship and Conservation": "agricultural-sciences/agricultural-stewardship-conservation-certificate/",
    "Biblical Studies": "liberal-arts/biblical-studies-certificate/",
    "Climate and Environmental Change": "earth-mineral-sciences/climate-environmental-change-certificate/",
    "Community Forestry": "agricultural-sciences/community-forestry-certificate/",
    "Development and Sustainability in Africa": "liberal-arts/development-sustainability-africa-certificate/",
    "Diversity Studies": "liberal-arts/diversity-studies-certificate/",
    "Earth Sustainability": "earth-mineral-sciences/earth-sustainability-certificate/",
    "Engineering and Community Engagement": "engineering/engineering-community-engagement-certificate/",
    "Engineering Design with Digital Tools": "engineering/engineering-design-digital-tools-certificate/",
    "Engineering Design": "engineering/engineering-design-certificate/",
    "Environment and Society Geography": "earth-mineral-sciences/environment-society-geography-certificate/",
    "Geographic Information Science": "earth-mineral-sciences/geographic-information-science-certificate/",
    "Geospatial Big Data Analytics": "earth-mineral-sciences/geospatial-big-data-analytics-certificate/",
    "Global Environmental Systems": "earth-mineral-sciences/global-environmental-systems-certificate/",
    "Health Care Administration": "health-human-development/health-care-administration-certificate/",
    "Health Policy": "health-human-development/health-policy-certificate/",
    "Holocaust and Genocide Studies": "liberal-arts/holocaust-genocide-studies-certificate/",
    "Housing": "engineering/housing-certificate/",
    "Information Sciences and Technology": "information-sciences-technology/information-sciences-technology-certificate/",
    "Instructor Development for Professionals": "education/instructor-development-professionals-certificate/",
    "International Engineering": "engineering/international-engineering-certificate/",
    "International Science": "eberly-science/international-science-certificate/",
    "Justice, Ethics": "earth-mineral-sciences/justice-ethics-diversity-space-certificate/",
    "Labor and Human Resources": "liberal-arts/labor-human-resources-certificate/",
    "Landscape Ecology": "earth-mineral-sciences/landscape-ecology-certificate/",
    "Landscapes: Societies, Cultures, and Political Economies": "earth-mineral-sciences/landscapes-societies-cultures-political-economies-certificate/",
    "Meeting and Event Management": "health-human-development/meeting-event-management-certificate/",
    "Museum Studies": "arts-architecture/museum-studies-certificate/",
    "Nanotechnology": "engineering/nanotechnology-certificate/",
    "National Security Agency": "information-sciences-technology/national-security-agency-certificate/",
    "Nursing Informatics": "nursing/nursing-informatics-certificate/",
    "Nursing Management": "nursing/nursing-management-certificate/",
    "Operational Excellence for Professionals": "education/operational-excellence-professionals-certificate/",
    "Organizational Communication": "liberal-arts/organizational-communication-certificate/",
    "Presidential Leadership Academy": "presidential-leadership-academy-certificate/",
    "Product Innovation Entrepreneurship": "engineering/product-innovation-entrepreneurship-certificate/",
    "Professional Snowsports Education": "health-human-development/professional-snowsports-education-certificate/",
    "Real Estate Analysis and Development": "smeal-business/real-estate-analysis-development-certificate/",
    "Science Research Distinction": "eberly-science/science-research-distinction-certificate/",
    "Small Group Conflict and Collaboration": "liberal-arts/small-group-conflict-collaboration-certificate/",
    "Smeal College Business Fundamentals": "smeal-business/smeal-college-business-fundamentals-certificate/",
    "Space Systems Engineering": "engineering/space-systems-engineering-certificate/",
    "Sports Journalism": "bellisario-communications/sports-journalism-certificate/",
    "Supervisory Leadership for Professionals": "education/supervisory-leadership-professionals-certificate/",
    "Worklink Strategies and Employability": "education/worklink-strategies-employability-certificate/",

    # Add more certificates here following the same pattern
}

# Directory to save CSVs for certificates
output_dir = "certificates_courses"
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

def scrape_certificate_courses(driver, certificate_name, certificate_url):
    """Scrapes program requirements and course data for a given certificate using Selenium."""
    # Clean the certificate_url by stripping leading/trailing spaces
    certificate_url = certificate_url.strip()
    # Build the full URL
    full_url = base_url + certificate_url

    logging.info(f"Accessing {certificate_name} at {full_url}")
    print(f"Accessing {certificate_name} at {full_url}")

    # Navigate to the page with proper error handling and waiting
    try:
        driver.get(full_url)
        # Wait until the 'Program Requirements' section is present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "programrequirementstextcontainer"))
        )
        time.sleep(2)  # Additional wait to ensure all dynamic content loads
    except Exception as e:
        logging.error(f"Error loading page for {certificate_name} at {full_url}: {e}")
        print(f"Error loading page for {certificate_name} at {full_url}: {e}")
        return

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize variables to store program requirements and course data
    total_credits = None
    program_policies = []
    required_courses = []
    selectable_groups = []
    current_select_group = None

    # ---------------------------
    # Extract Program Requirements
    # ---------------------------
    try:
        program_requirements_container = soup.find('div', id='programrequirementstextcontainer')
        if not program_requirements_container:
            logging.warning(f"'Program Requirements' container not found for {certificate_name}")
            print(f"'Program Requirements' container not found for {certificate_name}")
        else:
            # Extract total credits from the paragraph
            credits_paragraph = program_requirements_container.find('p', string=re.compile(r'minimum of\s+\d+\s+credits', re.I))
            if credits_paragraph:
                total_credits_match = re.search(r'minimum of\s+(\d+)', credits_paragraph.get_text(), re.I)
                if total_credits_match:
                    total_credits = int(total_credits_match.group(1))
                    logging.info(f"Total credits for {certificate_name}: {total_credits}")
                    print(f"Total credits for {certificate_name}: {total_credits}")
            else:
                logging.warning(f"No total credits information found for {certificate_name}")
                print(f"No total credits information found for {certificate_name}")

            # Extract program policies from paragraphs
            policies = program_requirements_container.find_all('p')
            for policy in policies:
                policy_text = clean_text(policy.get_text())
                program_policies.append(policy_text)
                logging.info(f"Program policy for {certificate_name}: {policy_text}")
                print(f"Program policy for {certificate_name}: {policy_text}")
    except Exception as e:
        logging.error(f"Error extracting program requirements for {certificate_name}: {e}")
        print(f"Error extracting program requirements for {certificate_name}: {e}")

    # ---------------------------
    # Extract Course Listings
    # ---------------------------
    try:
        # Find the 'Program Requirements' header
        requirements_header = program_requirements_container.find('h2', string=re.compile("Program Requirements", re.I))
        if not requirements_header:
            logging.warning(f"'Program Requirements' header not found for {certificate_name}")
            print(f"'Program Requirements' header not found for {certificate_name}")
        else:
            # The course list table is after the header
            course_table = requirements_header.find_next('table', class_='sc_courselist')
            if not course_table:
                logging.warning(f"No 'sc_courselist' table found for {certificate_name}")
                print(f"No 'sc_courselist' table found for {certificate_name}")
            else:
                tbody = course_table.find('tbody')
                if not tbody:
                    logging.warning(f"No table body found in 'sc_courselist' for {certificate_name}")
                    print(f"No table body found in 'sc_courselist' for {certificate_name}")
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
                                    # Combine course titles appropriately
                                    combined_titles = ' | '.join([clean_text(title_td.get_text())] * len(course_codes))
                                    course_title = combined_titles
                                else:
                                    course_title = clean_text(title_td.get_text())
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

                        # Handle rows that describe selection criteria without specific courses
                        # For example: "Select 0-3 credits of BMB courses at the 400-level"
                        description_directive = row.find('span', class_='courselistcomment')
                        if description_directive and 'select' in description_directive.text.lower():
                            selection_text = clean_text(description_directive.text)
                            select_number_match = re.search(r'Select\s+(\d+)(?:-\d+)?\s+credits?', selection_text, re.I)
                            if select_number_match:
                                select_number = select_number_match.group(1)
                            else:
                                select_number = 'N/A'
                            current_select_group = {
                                'Select_Number': select_number,
                                'Description': selection_text,
                                'Options': []
                            }
                            selectable_groups.append(current_select_group)
                            logging.info(f"Found selectable group: {selection_text}")
                            print(f"Found selectable group: {selection_text}")
                            continue

                        # This is a required course
                        logging.info(f"Handling required course row {idx}")
                        print(f"Handling required course row {idx}")
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
                        title_td = row.find('td', class_='titlecol')
                        if title_td:
                            course_title_text = clean_text(title_td.get_text())
                            if re.search(r'\bor\b', course_title_text, re.I):
                                # Combine course codes with '|'
                                combined_course_codes = ' | '.join(course_codes)
                                # Combine course titles appropriately
                                combined_titles = ' | '.join([clean_text(title_td.get_text())] * len(course_codes))
                                course_title = combined_titles
                            else:
                                course_title = clean_text(title_td.get_text())
                        else:
                            course_title = 'N/A'

                        # Extract credits
                        credits_td = row.find('td', class_='hourscol')
                        credits = clean_text(credits_td.get_text()) if credits_td else 'N/A'

                        for code in course_codes:
                            required_courses.append({
                                'Course_Code': code,
                                'Course_Title': course_title,
                                'Credits': credits
                            })
                            logging.info(f"Added required course: {code} - {course_title} ({credits} Credits)")
                            print(f"Added required course: {code} - {course_title} ({credits} Credits)")
    except Exception as e:
        logging.error(f"Error extracting course listings for {certificate_name}: {e}")
        print(f"Error extracting course listings for {certificate_name}: {e}")

    # ---------------------------
    # Prepare and Save Data
    # ---------------------------
    try:
        # Remove duplicate required courses if any
        unique_required = {tuple(course.items()) for course in required_courses}
        required_courses = [dict(t) for t in unique_required]

        # Prepare the final course list
        final_courses = {
            'Required Courses': required_courses,
            'Selectable Groups': selectable_groups
        }

        # Convert to DataFrame and save to CSV
        # First, create a DataFrame for required courses
        if final_courses['Required Courses']:
            df_required = pd.DataFrame(final_courses['Required Courses'])
            df_required['Type'] = 'Mandatory'
        else:
            df_required = pd.DataFrame(columns=['Course_Code', 'Course_Title', 'Credits', 'Type'])

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

        # Combine required and selectable DataFrames
        if not df_required.empty and not df_selectable.empty:
            df_all = pd.concat([df_required, df_selectable], ignore_index=True)
        elif not df_required.empty:
            df_all = df_required
        else:
            df_all = df_selectable

        # Add columns for Certificate, Total Credits, Program Policies, and URL
        df_all['Certificate'] = certificate_name
        df_all['Total_Credits'] = total_credits if total_credits else 'N/A'
        df_all['Program_Policies'] = '; '.join(program_policies) if program_policies else 'N/A'
        df_all['URL'] = full_url

        # Reorder columns for better readability
        df_all = df_all[['Certificate', 'Total_Credits', 'Course_Code', 'Course_Title', 'Credits', 'Type', 'Program_Policies', 'URL']]

        # Clean the certificate name for filename
        csv_filename = remove_parentheses(certificate_name).replace(' ', '_').replace('/', '_') + ".csv"
        csv_file = os.path.join(output_dir, csv_filename)
        df_all.to_csv(csv_file, index=False)
        logging.info(f"Saved {certificate_name} courses and requirements to {csv_file}")
        print(f"Saved {certificate_name} courses and requirements to {csv_file}")
    except Exception as e:
        logging.error(f"Error saving data for {certificate_name}: {e}")
        print(f"Error saving data for {certificate_name}: {e}")

def main():
    # Configure Selenium to use headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize the WebDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Scrape courses and program requirements for each certificate
        for certificate_name, certificate_url in certificates.items():
            print(f"\nScraping data for {certificate_name}...")
            logging.info(f"Scraping data for {certificate_name}")
            scrape_certificate_courses(driver, certificate_name, certificate_url)
            time.sleep(2)  # Delay to be respectful to the server
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
