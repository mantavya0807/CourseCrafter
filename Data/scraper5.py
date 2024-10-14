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
   "Acturial Science B.S. ": "smeal-business/actuarial-science-bs/ ",
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
   "Energy Engineering B.S.:": "earth-mineral-sciences/energy-engineering-bs/",
   "Engineering Science B.S.": "engineering/engineering-science-bs/",
   "English B.A.": "liberal-arts/english-ba/",
   "Enterprise Technology Integration B.S." : "information-sciences-technology/enterprise-technology-integration-bs/",
   "Environmental Resource Management B.S.": "agricultural-sciences/environmental-resource-management-bs/",
   "Environmental Systems Engineering B.S.": "environmental-systems-engineering-bs/",
   "Film Production B.A.": "bellisario-communications/film-production-ba/",
   "Finance B.S.": "smeal-business/finance-bs/",
   "Food Science B.S.":  "agricultural-sciences/food-science-bs/",
   "Forestry B.S.":"agricultural-sciences/forest-ecosystem-management-bs/",
   "French B.A.": "liberal-arts/french-francophone-studies-ba/",
   "General Science B.S.":"eberly-science/integrative-science-bs/",
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
   "Philosophy B.A.": "/liberal-arts/philosophy-ba/",
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
   "World Language Education B.S.":"education/world-languages-k-12-education-bs/"
   # Add more majors here following the same pattern
}

# Directory to save CSVs
output_dir = "majors_courses"
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

def extract_courses_from_cell(cell):
    """
    Extracts course codes and titles from a table cell.
    Handles multiple courses and 'or' conditions.
    Returns a list of dictionaries with Course_Code and Course_Title.
    """
    courses = []
    # First, find all linked courses
    links = cell.find_all('a', class_='bubblelink code')
    if links:
        for link in links:
            course_code = clean_text(link.get_text())
            # Extract the full title by removing the link
            link.extract()
            course_title = clean_text(cell.get_text())
            courses.append({
                'Course_Code': course_code,
                'Course_Title': course_title
            })
    else:
        # If no links, attempt to split courses by 'or' or ','
        cell_text = clean_text(cell.get_text())
        # Remove superscripts and footnotes
        cell_text = re.sub(r'\s*<sup>.*?</sup>', '', cell_text)
        # Split by 'or' first
        or_split = split_courses(cell_text)
        for part in or_split:
            # Further split by comma if necessary
            comma_split = part.split(',')
            for course in comma_split:
                course = course.strip()
                if course:
                    courses.append({
                        'Course_Code': '',
                        'Course_Title': course
                    })
    return courses

def scrape_mandatory_and_selectable_courses(soup):
    """
    Scrapes mandatory and selectable courses from the 'sc_courselist' table.
    Returns two lists: mandatory_courses and selectable_groups.
    """
    mandatory_courses = []
    selectable_groups = []
    current_select_group = None

    # Find the 'Requirements for the Major' section
    requirements_toggle = soup.find('button', string=re.compile("Requirements for the Major", re.I))
    if not requirements_toggle:
        print(f"'Requirements for the Major' toggle not found.")
        return mandatory_courses, selectable_groups

    # The toggle content is within the next sibling div with class 'toggle-content'
    toggle_parent = requirements_toggle.find_parent('h3')
    if not toggle_parent:
        print(f"Parent <h3> tag not found for 'Requirements for the Major'.")
        return mandatory_courses, selectable_groups
    toggle_content = toggle_parent.find_next_sibling('div', class_='toggle-content')
    if not toggle_content:
        print(f"No toggle content found for 'Requirements for the Major'.")
        return mandatory_courses, selectable_groups

    # Find the 'sc_courselist' table
    course_table = toggle_content.find('table', class_='sc_courselist')
    if not course_table:
        print(f"No course table found in 'Requirements for the Major'.")
        return mandatory_courses, selectable_groups

    # Iterate over each row in the table body
    tbody = course_table.find('tbody')
    if not tbody:
        print(f"No table body found in course table.")
        return mandatory_courses, selectable_groups

    rows = tbody.find_all('tr')
    for idx, row in enumerate(rows, start=1):
        row_classes = row.get('class', [])

        # Debug: Print row number and classes
        print(f"Processing row {idx} with classes: {row_classes}")

        # Skip header rows or area headers
        if 'areaheader' in row_classes or 'areasubheader' in row_classes:
            print(f"Skipping header row {idx}")
            continue

        # Check if the row contains a 'Select X' directive
        select_directive = row.find('span', string=re.compile(r'Select\s+\d+', re.I))
        if select_directive:
            # Extract the number of courses to select
            select_number_match = re.search(r'Select\s+(\d+)', select_directive.text, re.I)
            if select_number_match:
                select_number = int(select_number_match.group(1))
                current_select_group = {
                    'Select_Number': select_number,
                    'Options': []
                }
                selectable_groups.append(current_select_group)
                print(f"Found selectable group: Select {select_number} course(s) from the following:")
            continue  # Move to the next row

        # Handle 'orclass' rows
        if 'orclass' in row_classes:
            print(f"Handling 'orclass' row {idx}")
            # This row contains alternative course options
            code_col = row.find('td', class_='codecol orclass')
            title_col = row.find('td', colspan='2')  # Correct selector for 'orclass' rows

            if not code_col or not title_col:
                print(f"Missing code or title column in 'orclass' row {idx}")
                continue  # Skip if necessary columns are missing

            # Extract all courses from code_col
            courses = extract_courses_from_cell(code_col)
            for course in courses:
                course_code = course['Course_Code']
                course_title = course['Course_Title']
                # Extract credits
                credits_col = row.find('td', class_='hourscol')
                credits = clean_text(credits_col.get_text(strip=True)) if credits_col else 'N/A'

                # Append each course as part of the current select group if it exists
                if current_select_group:
                    current_select_group['Options'].append({
                        'Course_Code': course_code,
                        'Course_Title': course_title,
                        'Credits': credits
                    })
                    print(f"Added selectable course (alternative): {course_code} - {course_title} ({credits} Credits)")
                else:
                    # If no current select group, treat as a standalone selectable group with Select 1
                    standalone_select_group = {
                        'Select_Number': 1,
                        'Options': [{
                            'Course_Code': course_code,
                            'Course_Title': course_title,
                            'Credits': credits
                        }]
                    }
                    selectable_groups.append(standalone_select_group)
                    print(f"Added standalone selectable group: Select 1 course - {course_code} - {course_title} ({credits} Credits)")
            continue  # Move to the next row

        # Handle selectable options (indented)
        block_indent = row.find('div', class_='blockindent')
        if block_indent:
            # This is a selectable option within a selectable group
            courses = extract_courses_from_cell(block_indent)
            # Extract course title and credits
            title_td = row.find('td', class_='titlecol')
            if title_td:
                course_title = clean_text(title_td.get_text())
            else:
                # Attempt to extract from the second 'td' if available
                all_tds = row.find_all('td')
                if len(all_tds) >= 2:
                    course_title = clean_text(all_tds[1].get_text())
                else:
                    course_title = 'N/A'

            # Extract credits
            credits_td = row.find('td', class_='hourscol')
            credits = clean_text(credits_td.get_text(strip=True)) if credits_td else 'N/A'

            # Add to the current selectable group
            if current_select_group:
                for course in courses:
                    current_select_group['Options'].append({
                        'Course_Code': course['Course_Code'],
                        'Course_Title': course['Course_Title'],
                        'Credits': credits
                    })
                    print(f"Added selectable course: {course['Course_Code']} - {course['Course_Title']} ({credits} Credits)")
            else:
                # Edge case: selectable option without a preceding select directive
                print(f"Selectable course found without a selection group: {courses}")
            continue  # Move to the next row

        # Otherwise, treat as a mandatory course
        print(f"Handling mandatory course row {idx}")
        code_col = row.find('td', class_='codecol')
        if not code_col:
            print(f"Skipping row {idx} as 'codecol' not found.")
            continue

        # Extract all courses from code_col
        courses = extract_courses_from_cell(code_col)

        # Extract course title
        title_td = row.find('td', class_='titlecol')
        if title_td:
            # Remove any images or additional tags (e.g., Keystone icons) from the title
            for img in title_td.find_all('img'):
                img.decompose()
            course_title = clean_text(title_td.get_text())
        else:
            # Attempt to extract from the second 'td' if available
            all_tds = row.find_all('td')
            if len(all_tds) >= 2:
                course_title = clean_text(all_tds[1].get_text())
            else:
                course_title = 'N/A'

        # Extract credits
        credits_td = row.find('td', class_='hourscol')
        credits = clean_text(credits_td.get_text(strip=True)) if credits_td else 'N/A'

        for course in courses:
            course_code = course['Course_Code']
            course_title = course['Course_Title']
            mandatory_courses.append({
                'Course_Code': course_code,
                'Course_Title': course_title,
                'Credits': credits
            })
            print(f"Added mandatory course: {course_code} - {course_title} ({credits} Credits)")

    # Remove duplicate mandatory courses if any
    unique_mandatory = {tuple(course.items()) for course in mandatory_courses}
    mandatory_courses = [dict(t) for t in unique_mandatory]

    return mandatory_courses, selectable_groups

def scrape_academic_plan(soup):
    """
    Scrapes the Suggested Academic Plan from the 'sc_plangrid' table.
    Returns a list of academic_plan_courses with Year and Semester.
    """
    academic_plan_courses = []
    current_year = None
    current_semesters = []

    # Find the 'Suggested Academic Plan' section
    # Assuming it's the second 'toggle-content' div or similar
    plan_table = soup.find('table', class_='sc_plangrid')
    if not plan_table:
        print(f"No academic plan table found.")
        return academic_plan_courses

    # Iterate over each row in the table body
    tbody = plan_table.find('tbody')
    if not tbody:
        print(f"No table body found in academic plan table.")
        return academic_plan_courses

    rows = tbody.find_all('tr')
    for idx, row in enumerate(rows, start=1):
        row_classes = row.get('class', [])

        # Debug: Print row number and classes
        print(f"Processing academic plan row {idx} with classes: {row_classes}")

        # Check for Year headers
        if 'plangridyear' in row_classes:
            year_text = row.get_text(strip=True)
            current_year = clean_text(year_text)
            print(f"Found Year: {current_year}")
            continue

        # Check for Semester headers
        if 'plangridterm' in row_classes:
            semester_headers = row.find_all('th', class_='plangridtermhdr')
            current_semesters = [clean_text(th.get_text()) for th in semester_headers]
            print(f"Found Semesters: {current_semesters}")
            continue

        # Skip summary or total rows
        if 'plangridsum' in row_classes or 'plangridtotal' in row_classes:
            print(f"Skipping summary/total row {idx}")
            continue

        # Process course rows
        if 'plangridterm' not in row_classes and 'plangridyear' not in row_classes:
            # Expecting four cells: Fall Code, Fall Credits, Spring Code, Spring Credits
            cells = row.find_all('td')
            if len(cells) < 4:
                print(f"Skipping row {idx} due to insufficient cells.")
                continue

            # Extract Fall courses and credits
            fall_cell = cells[0]
            fall_courses = extract_courses_from_cell(fall_cell)
            fall_credits = clean_text(cells[1].get_text()) if len(cells) >= 2 else 'N/A'

            # Extract Spring courses and credits
            spring_cell = cells[2]
            spring_courses = extract_courses_from_cell(spring_cell)
            spring_credits = clean_text(cells[3].get_text()) if len(cells) >= 4 else 'N/A'

            # Assign semesters based on headers
            if len(current_semesters) >= 2:
                fall_semester = current_semesters[0]
                spring_semester = current_semesters[1]
            else:
                # Default to Fall and Spring if headers are missing
                fall_semester = 'Fall'
                spring_semester = 'Spring'

            # Add Fall courses
            for course in fall_courses:
                course_code = course['Course_Code']
                course_title = course['Course_Title']
                academic_plan_courses.append({
                    'Course_Code': course_code,
                    'Course_Title': course_title,
                    'Credits': fall_credits,
                    'Year': current_year,
                    'Semester': fall_semester
                })
                print(f"Added academic plan course: {course_code} - {course_title} ({fall_credits} Credits) [{current_year} - {fall_semester}]")

            # Add Spring courses
            for course in spring_courses:
                course_code = course['Course_Code']
                course_title = course['Course_Title']
                academic_plan_courses.append({
                    'Course_Code': course_code,
                    'Course_Title': course_title,
                    'Credits': spring_credits,
                    'Year': current_year,
                    'Semester': spring_semester
                })
                print(f"Added academic plan course: {course_code} - {course_title} ({spring_credits} Credits) [{current_year} - {spring_semester}]")

    # Remove duplicate academic plan courses if any
    unique_academic = {tuple(course.items()) for course in academic_plan_courses}
    academic_plan_courses = [dict(t) for t in unique_academic]

    return academic_plan_courses

def scrape_major_courses(driver, major_name, major_url):
    """Scrapes course data for a given major using Selenium."""
    # Clean the major_url by stripping leading/trailing spaces
    major_url = major_url.strip()
    # Build the full URL
    full_url = base_url + major_url

    print(f"Accessing {major_name} at {full_url}")

    # Navigate to the page with proper error handling and waiting
    try:
        driver.get(full_url)
        # Wait until the 'Requirements for the Major' section is present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Requirements for the Major')]"))
        )
        time.sleep(2)  # Additional wait to ensure all dynamic content loads
    except Exception as e:
        print(f"Error loading page for {major_name} at {full_url}: {e}")
        return

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Scrape mandatory and selectable courses
    mandatory_courses, selectable_groups = scrape_mandatory_and_selectable_courses(soup)

    # Scrape the academic plan
    academic_plan_courses = scrape_academic_plan(soup)

    # Remove duplicate mandatory courses if any
    unique_mandatory = {tuple(course.items()) for course in mandatory_courses}
    mandatory_courses = [dict(t) for t in unique_mandatory]

    # Prepare the final course list
    # Create a DataFrame for mandatory courses
    if mandatory_courses:
        df_mandatory = pd.DataFrame(mandatory_courses)
        df_mandatory['Type'] = 'Mandatory'
        df_mandatory['Year'] = ''
        df_mandatory['Semester'] = ''
    else:
        df_mandatory = pd.DataFrame(columns=['Course_Code', 'Course_Title', 'Credits', 'Type', 'Year', 'Semester'])

    # Create a DataFrame for selectable groups
    selectable_data = []
    for group in selectable_groups:
        select_num = group['Select_Number']
        for option in group['Options']:
            selectable_data.append({
                'Course_Code': option['Course_Code'],
                'Course_Title': option['Course_Title'],
                'Credits': option['Credits'],
                'Type': f'Select {select_num}',
                'Year': '',
                'Semester': ''
            })

    if selectable_data:
        df_selectable = pd.DataFrame(selectable_data)
    else:
        df_selectable = pd.DataFrame(columns=['Course_Code', 'Course_Title', 'Credits', 'Type', 'Year', 'Semester'])

    # Create a DataFrame for academic plan courses
    if academic_plan_courses:
        df_academic = pd.DataFrame(academic_plan_courses)
        df_academic['Type'] = 'Academic Plan'
    else:
        df_academic = pd.DataFrame(columns=['Course_Code', 'Course_Title', 'Credits', 'Type', 'Year', 'Semester'])

    # Combine all DataFrames
    df_all = pd.concat([df_mandatory, df_selectable, df_academic], ignore_index=True)

    # Add columns for Major and URL
    df_all['Major'] = major_name
    df_all['URL'] = full_url

    # Reorder columns for better readability
    df_all = df_all[['Major', 'Course_Code', 'Course_Title', 'Credits', 'Type', 'Year', 'Semester', 'URL']]

    # Clean the major name for filename
    csv_filename = remove_parentheses(major_name).replace(' ', '_').replace('/', '_') + ".csv"
    csv_file = os.path.join(output_dir, csv_filename)
    df_all.to_csv(csv_file, index=False)
    print(f"Saved {major_name} courses to {csv_file}")

def main():
    # Configure Selenium to use headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize the WebDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Scrape courses for each major
        for major_name, major_url in majors.items():
            print(f"\nScraping courses for {major_name}...")
            scrape_major_courses(driver, major_name, major_url)
            time.sleep(2)  # Delay to be respectful to the server
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
