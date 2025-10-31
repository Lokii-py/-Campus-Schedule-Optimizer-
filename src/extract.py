import re
from pathlib import Path
import pandas as pd

def extract_schedule_data(filename: Path, course: str) -> pd.DataFrame:
    """
    It scans the text file for a course title (our 'landmark'), then looks for a 5-digit class number
    (the 'start' of a block). Once it finds a block, it grabs all the
    details (time, room, instructors) until it hits the date line
    (the 'end'). Returns a pandas DataFrame with all the extracted class sections.
    """
    
    # Define the regex pattern
    
    # Group 1: (ENG MGT 1210) | Group 2: (Economic Analysis of...) - the course title
    course_pattern = re.compile(rf"({course} \d{{4}}) - (.*)")
    
    # starting signal: five digit class number like 71016
    class_num_pattern = re.compile(r"^\d{5}$")
    
    # ending signal : e.g., "08/25/2025 - 12/12/2025"
    date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4}$")

    # Make a dictionary for every course
    extracted_data = []
    
    try:
        with open(filename, 'r') as f:
            # Store all the lines in the lines list
            lines = [line.strip() for line in f.readlines()] 

        # Placeholder for coure name
        current_course_code = "Lokesh"
        current_course_title = "Lokesh"

        for i, line in enumerate(lines):
            
            course_match = course_pattern.search(line)
            if course_match:
                current_course_code = course_match.group(1)
                current_course_title = course_match.group(2).split(" Collapsible")[0]
                continue

            # Check the 5 digit code 
            class_num_match = class_num_pattern.search(line)
            if class_num_match:
                
                try:
                    class_number = line
                    section = lines[i + 1]
                    days_times = lines[i + 3]
                    room = lines[i + 4]
                    
                    instructor_list = []

                    for j in range(i + 5, i + 10):
                        if date_pattern.search(lines[j]):
                            break
                        else:
                            instructor_list.append(lines[j])
                    
                    instructors = ", ".join(instructor_list)

                    # Store the dictionary in the extracted list
                    extracted_data.append({
                        "Course Code": current_course_code,
                        "Course Title": current_course_title,
                        "Class #": class_number,
                        "Section": section,
                        "Days & Times": days_times,
                        "Room": room,
                        "Instructors": instructors
                    })
                        
                except IndexError:
                    continue

        # Create a data frame form the extracted_data
        df = pd.DataFrame(extracted_data)
        print(f"Successfully extracted {len(df)} total class sections.")
        return df

    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return pd.DataFrame() # Return an empty DataFrame on error
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()