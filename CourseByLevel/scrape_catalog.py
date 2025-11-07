import requests
from bs4 import BeautifulSoup

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

if nav_list:
    print("Successfully found the nav list")
    all_links = nav_list.find_all('a', href=True)

    print(f"found all {len(all_links)} in the given url")

    base_url = "https://catalog.mst.edu"
    program_url = []

    for link in all_links:
        relative_path = link['href']
        full_url = base_url + relative_path + "#bachelorstext"
        program_url.append(full_url)

    print("DEBUG: URL number : ", len(program_url))

    # for url in program_url[:5]:
    #     print(url)

    # for link in all_links[:5]:
    #     print(link['href'])
else:
    print("Error: There is no nav list")

try:
    for url in program_url:
        try:

            course_url = url
            response = requests.get(course_url)
            response.raise_for_status()

        except requests.RequestException as e:
            print(f"Couldn't download this url - {url}")
            print(f"There is an error associated with this: {e}")
            continue 

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='sc_plangrid')

        if table:
            print("found table in", url)
        else :
            with open("no_table.txt", 'a') as f:
                f.write(f"Skipping {url}\n")
            print(f"Skipping {url} (No table found.)")
            continue

except Exception as e:
    print(f"Error: {e}")