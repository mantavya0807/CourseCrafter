import pandas as pd
import re
import os
import glob

# Define the directories
input_directory = 'majors_courses'
output_directory = 'majors_courses_refined'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)    

# Define expected columns in lowercase for normalization
expected_columns = ['major', 'course_code', 'course_title', 'credits', 'type', 'year', 'semester', 'url']

# Function to clean text by removing annotations, footnotes, and unwanted characters
def clean_text(text):
    if isinstance(text, str):
        # Remove text within parentheses
        text = re.sub(r'\(.*?\)', '', text)
        # Remove *, #, and other unwanted characters (including specific non-ASCII characters)
        text = re.sub(r'[;*\#â€¡â€ ]', '', text)  # Added ';' and adjusted for multiple special chars
        # Remove 'Â' and trim spaces
        text = text.replace('Â', '').strip()
    else:
        text = ''
    return text

# Function to split 'or' and '&' conditions in Course_Code and Course_Title
def split_or_conditions(row):
    course_codes = []
    course_titles = []
    
    # Handle Course_Code
    course_code = row.get('course_code', '')
    if isinstance(course_code, str) and re.search(r'\b(or|&)\b', course_code, re.I):
        # Split by 'or' or '&' with surrounding spaces
        parts = re.split(r'\s+\b(or|&)\b\s+', course_code, flags=re.I)
        # Extract course codes, skipping 'or'/'&'
        course_codes.extend([part.strip() for part in parts if part.lower() not in ['or', '&']])
    elif isinstance(course_code, str):
        course_codes.append(course_code.strip())
    
    # Handle Course_Title
    course_title = row.get('course_title', '')
    if isinstance(course_title, str) and re.search(r'\b(or|&)\b', course_title, re.I):
        parts = re.split(r'\s+\b(or|&)\b\s+', course_title, flags=re.I)
        course_titles.extend([part.strip() for part in parts if part.lower() not in ['or', '&']])
    elif isinstance(course_title, str):
        course_titles.append(course_title.strip())
    
    # If Course_Title is missing or less than Course_Code, fill with empty strings
    while len(course_titles) < len(course_codes):
        course_titles.append('')
    
    # Create new rows
    new_rows = []
    for code, title in zip(course_codes, course_titles):
        if code:  # Ensure Course_Code is not empty
            new_rows.append({
                'major': row['major'],
                'course_code': code,
                'course_title': title,
                'credits': row['credits'],
                'type': row['type'],
                'year': row['year'],
                'semester': row['semester'],
                'url': row['url']
            })
    return pd.DataFrame(new_rows)

# Function to further split Course_Code and Course_Title if they still contain 'or' or '&'
def further_split_course_code(row):
    course_codes = []
    course_titles = []
    
    # Handle Course_Code
    course_code = row.get('course_code', '')
    if isinstance(course_code, str) and re.search(r'\b(or|&)\b', course_code, re.I):
        parts = re.split(r'\s+\b(or|&)\b\s+', course_code, flags=re.I)
        course_codes.extend([part.strip() for part in parts if part.lower() not in ['or', '&']])
    elif isinstance(course_code, str):
        course_codes.append(course_code.strip())
    
    # Handle Course_Title
    course_title = row.get('course_title', '')
    if isinstance(course_title, str) and re.search(r'\b(or|&)\b', course_title, re.I):
        parts = re.split(r'\s+\b(or|&)\b\s+', course_title, flags=re.I)
        course_titles.extend([part.strip() for part in parts if part.lower() not in ['or', '&']])
    elif isinstance(course_title, str):
        course_titles.append(course_title.strip())
    
    # If Course_Title is missing or less than Course_Code, fill with empty strings
    while len(course_titles) < len(course_codes):
        course_titles.append('')
    
    # Create new rows
    new_rows = []
    for code, title in zip(course_codes, course_titles):
        if code:  # Ensure Course_Code is not empty
            new_rows.append({
                'major': row['major'],
                'course_code': code,
                'course_title': title,
                'credits': row['credits'],
                'type': row['type'],
                'year': row['year'],
                'semester': row['semester'],
                'url': row['url']
            })
    return pd.DataFrame(new_rows)

# Function to create binary indicators for Types
def separate_types(types):
    indicators = {'Mandatory': 0, 'Select': 0, 'Academic_Plan': 0}
    if isinstance(types, str):
        # Split by semicolon and strip whitespace
        types_list = [t.strip() for t in types.split(';')]
        for t in types_list:
            if 'Mandatory' in t:
                indicators['Mandatory'] = 1
            if 'Select' in t:
                indicators['Select'] = 1
            if 'Academic Plan' in t:
                indicators['Academic_Plan'] = 1
    return indicators

# Function to log DataFrame info for debugging
def log_dataframe_info(df, stage, filename):
    print(f"\n--- {stage} --- for file: {filename} ---")
    print(f"Number of rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    # Uncomment the following line to print the first few rows
    # print(df.head())

# Iterate through all CSV files in the input directory
csv_files = glob.glob(os.path.join(input_directory, '*.csv'))

for file_path in csv_files:
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        original_filename = os.path.basename(file_path)
        print(f"\nProcessing file: {original_filename}")
        
        # Normalize column names: strip whitespace and convert to lowercase
        df.columns = df.columns.str.strip().str.lower()
        
        # Print column names for debugging
        log_dataframe_info(df, "Initial DataFrame", original_filename)
        
        # Check for missing expected columns
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            print(f"Error: Missing columns {missing_columns} in file {original_filename}. Skipping this file.")
            continue  # Skip this file and continue with the next
        
        # Clean the 'course_code' and 'course_title' columns
        df['course_code'] = df['course_code'].apply(clean_text)
        df['course_title'] = df['course_title'].apply(clean_text)
        
        # Clean the 'credits' column to retain only numerical values (including decimal points)
        df['credits'] = df['credits'].apply(lambda x: re.sub(r'[^0-9\.]', '', str(x)) if pd.notnull(x) else '')
        
        log_dataframe_info(df, "After Cleaning 'course_code', 'course_title', and 'credits'", original_filename)
        
        # Split 'or' conditions into separate rows using iterative approach
        expanded_dataframes = []
        for index, row in df.iterrows():
            expanded_df = split_or_conditions(row)
            if not expanded_df.empty:
                expanded_dataframes.append(expanded_df)
        
        if not expanded_dataframes:
            print(f"No data after splitting 'or' conditions in file {original_filename}. Skipping this file.")
            continue  # Skip to next file if no data is present
        
        # Concatenate all the resulting DataFrames
        df_expanded = pd.concat(expanded_dataframes, ignore_index=True)
        log_dataframe_info(df_expanded, "After First Splitting 'or' Conditions", original_filename)
        
        # Ensure 'course_code' column exists
        if 'course_code' not in df_expanded.columns:
            print(f"Error: 'course_code' column missing after splitting in file {original_filename}. Skipping this file.")
            continue
        
        # Remove rows with empty or 'N/A' Course_Code
        df_expanded = df_expanded[df_expanded['course_code'].str.strip() != '']
        df_expanded = df_expanded[~df_expanded['course_code'].str.contains(r'\bN/A\b', case=False, na=False)]
        
        # **New Filtering Step: Remove rows where course_code starts with a number**
        df_expanded = df_expanded[~df_expanded['course_code'].str.match(r'^\d')]
        print(f"Removed rows where 'course_code' starts with a number.")
        
        log_dataframe_info(df_expanded, "After Removing Empty, 'N/A', and Numeric-starting 'course_code'", original_filename)
        
        # Remove duplicate rows
        df_expanded = df_expanded.drop_duplicates()
        log_dataframe_info(df_expanded, "After Dropping Duplicates", original_filename)
        
        # Further split Course_Code and Course_Title if they still contain 'or' or '&'
        further_expanded_dataframes = []
        for index, row in df_expanded.iterrows():
            further_expanded_df = further_split_course_code(row)
            if not further_expanded_df.empty:
                further_expanded_dataframes.append(further_expanded_df)
        
        if further_expanded_dataframes:
            df_further_expanded = pd.concat(further_expanded_dataframes, ignore_index=True)
            log_dataframe_info(df_further_expanded, "After Further Splitting 'or'/'&' Conditions", original_filename)
        else:
            df_further_expanded = df_expanded.copy()
            log_dataframe_info(df_further_expanded, "No Further Splitting Needed", original_filename)
        
        # Ensure 'course_code' column exists after further splitting
        if 'course_code' not in df_further_expanded.columns:
            print(f"Error: 'course_code' column missing after further splitting in file {original_filename}. Skipping this file.")
            continue
        
        # Remove rows with empty Course_Code after splitting
        df_further_expanded = df_further_expanded[df_further_expanded['course_code'].str.strip() != '']
        
        # **Apply the same numeric-starting 'course_code' filter after further splitting**
        df_further_expanded = df_further_expanded[~df_further_expanded['course_code'].str.match(r'^\d')]
        print(f"Removed rows where 'course_code' starts with a number after further splitting.")
        
        log_dataframe_info(df_further_expanded, "After Removing Empty and Numeric-starting 'course_code' Post-Further Splitting", original_filename)
        
        # **Additional Filtering Step: Remove rows where course_title contains any course_code**
        # Get unique course_codes from course_title
        unique_course_codes = df_further_expanded['course_title'].dropna().unique()
        
        if len(unique_course_codes) > 0:
            # Escape regex special characters
            escaped_course_codes = [re.escape(code) for code in unique_course_codes]
            
            # Combine into a regex pattern
            pattern = '|'.join(escaped_course_codes)
            
            # Use str.contains to find rows where course_title contains any course_code
            # Since we want to delete rows where course_title contains course_code,
            # we need to delete rows where 'course_code' contains any of these codes
            mask = df_further_expanded['course_code'].str.contains(pattern, case=False, regex=True, na=False)
            
            # Count how many rows match
            rows_to_delete = mask.sum()
            
            # Delete those rows
            df_further_expanded = df_further_expanded[~mask]
            
            print(f"Removed {rows_to_delete} rows where 'course_code' contains a course_code from 'course_title'.")
            log_dataframe_info(df_further_expanded, "After Removing Rows with course_code Matching course_title Codes", original_filename)
        else:
            print("No course_codes available for additional filtering.")
        
        # Remove duplicate rows again
        df_further_expanded = df_further_expanded.drop_duplicates()
        log_dataframe_info(df_further_expanded, "After Dropping Duplicates Again", original_filename)
        
        # Group by Major and Course_Code to combine duplicate Course_Code entries
        grouped = df_further_expanded.groupby(['major', 'course_code'])
        
        # Aggregate the data
        df_grouped = grouped.agg({
            'course_title': lambda x: '; '.join(x.dropna().unique()),
            'credits': lambda x: '; '.join(x.dropna().unique()),
            'type': lambda x: '; '.join(x.dropna().unique()),
            'year': lambda x: '; '.join(x.dropna().unique()),
            'semester': lambda x: '; '.join(x.dropna().unique()),
            'url': 'first'  # Assuming URL is the same for all entries
        }).reset_index()
        
        log_dataframe_info(df_grouped, "After Grouping and Aggregation", original_filename)
        
        # Apply the separation for Type into binary indicators
        type_separated = df_grouped['type'].apply(separate_types).apply(pd.Series)
        df_grouped = pd.concat([df_grouped, type_separated], axis=1)
        
        log_dataframe_info(df_grouped, "After Separating 'type' into Indicators", original_filename)
        
        # Reorder and select relevant columns
        try:
            df_final = df_grouped[['major', 'course_code', 'course_title', 'credits', 'Mandatory', 'Select', 'Academic_Plan', 'year', 'semester', 'url']]
        except KeyError as e:
            print(f"Error: Missing expected column during final selection: {e} in file {original_filename}. Skipping this file.")
            continue
        
        # Final clean-up: trim whitespace and replace empty strings with NaN
        for col in ['major', 'course_code', 'course_title', 'year', 'semester', 'url']:
            df_final[col] = df_final[col].astype(str).str.strip()
            df_final[col] = df_final[col].replace('', pd.NA)
        
        log_dataframe_info(df_final, "Final Cleaned DataFrame", original_filename)
        
        # Save the refined DataFrame to a new CSV in the output directory
        filename, ext = os.path.splitext(original_filename)
        refined_filename = f"{filename}_refined{ext}"  # Added '_refined' back for clarity
        refined_file_path = os.path.join(output_directory, refined_filename)
        df_final.to_csv(refined_file_path, index=False)
        
        print(f"Successfully processed and saved: {refined_filename}")
    
    except Exception as e:
        print(f"An error occurred while processing file {original_filename}: {e}")
        continue  # Continue with the next file

print("\nAll files have been processed.")
