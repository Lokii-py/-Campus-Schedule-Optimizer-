import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://catalog.mst.edu/undergraduate/degreeprogramsandcourses/"

try:
    response = requests.get(url)
    response.raise_for_status()
    print("Downloaded Successfully")
except requests.RequestException as e:
    print(f"Couldn't download the page: {e}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

nav_list = soup.find("ul", class_="nav leveltwo")

programData = []

if nav_list:
    print("Successfully found the nav list")
    all_links = nav_list.find_all('a', href=True)
    print(f"found all {len(all_links)} in the given url")

    base_url = "https://catalog.mst.edu"

    for link in all_links:
        programName = link.text.strip()
        relative_path = link['href']
        full_url = base_url + relative_path + "#bachelorstext"
        
        programData.append((programName, full_url))

    print("DEBUG: URL number : ", len(programData))
else:
    print("Error: There is no nav list")


output_dir = "Program_CSVs"
os.makedirs(output_dir, exist_ok=True)
print(f"Saving files to '{output_dir}' folder")

try:
    for program_name, url in programData:
        
        print(f"Processing: {program_name}")
        
        try:
            course_url = url
            response = requests.get(course_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Couldn't download this url - {url}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='sc_plangrid')

        if table:
            print("found table in", url)
            
            all_scraped_courses = []
            
            all_rows = table.find_all('tr')
            current_year = 'unknown year'

            for row in all_rows:
                header_cell = row.find_all('th')
                if len(header_cell) == 1:
                    current_year = header_cell[0].text.strip()
                    continue
                if len(header_cell) > 1:
                    continue

                cells = row.find_all('td')

                if len(cells) >= 2:
                    courseCode1 = cells[0].text.strip().replace('\xa0', ' ')
                    courseCredit1 = cells[1].text.strip()
                    
                    if ' ' in courseCode1 and any(char.isdigit() for char in courseCode1):
                        all_scraped_courses.append({
                            "Program": program_name,
                            "Year": current_year,
                            "Semester": "First Semester",
                            "Course Code": courseCode1,
                            "Credits": courseCredit1
                        })

                if len(cells) >= 4:
                    courseCode2 = cells[2].text.strip().replace('\xa0', ' ')
                    courseCredit2 = cells[3].text.strip()

                    if ' ' in courseCode2 and any(char.isdigit() for char in courseCode2):
                        all_scraped_courses.append({
                            "Program": program_name,
                            "Year": current_year,
                            "Semester": "Second Semester",
                            "Course Code": courseCode2,
                            "Credits": courseCredit2
                        })
            
            if all_scraped_courses:
                df = pd.DataFrame(all_scraped_courses)
                
                safe_filename = program_name.replace(' ', '_').replace(',', '').replace('&', 'and') + ".csv"
                output_path = os.path.join(output_dir, safe_filename)
                
                df.to_csv(output_path, index=False)
                print(f"Successfully saved {safe_filename}")
            else:
                print("No courses found in this table.")

        else :
            with open("no_table.txt", 'a') as f:
                f.write(f"Skipping {program_name} ({url})\n")
            print(f"Skipping {program_name} (No table found.)")
            continue

except Exception as e:
    print(f"An error occurred: {e}")