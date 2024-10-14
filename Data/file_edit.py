import os
import csv
import re

 
current_dir = os.path.dirname(os.path.abspath(__file__))


input_folder = os.path.join(current_dir, 'majors_courses_refined')
output_folder = os.path.join(current_dir, 'majors_courses_suryansh')


if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def process_course_names(course_name):
    return re.sub(r'(\w+/\w+)\s(\d+)', lambda match: ' | '.join([f"{match.group(1).split('/')[0]} {match.group(2)}", f"{match.group(1).split('/')[1]} {match.group(2)}"]), course_name)


if os.path.exists(input_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):  
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)

           
            with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file:
                reader = csv.reader(input_file)
                rows = list(reader)  

            
            with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
                writer = csv.writer(output_file)

                
                for row in rows:
                    
                    new_row = [process_course_names(cell) for cell in row]
                    writer.writerow(new_row)

    print(f"All CSV files have been processed and saved in the folder: {output_folder}")
else:
    print(f"Input folder '{input_folder}' not found. Please make sure the folder exists.")

