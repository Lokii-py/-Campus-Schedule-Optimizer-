import re

def extract_schedule_text(filename:str, course: str):
    """
    Reads a schedule text file line by line. Identifies and prints lines
    that contain a course code matching the pattern provided in the parameters followed
    by four digits.
    """

    count = 0
    extrated_line = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                match = re.search(r"{course} \d{4}", line)
                if match:
                    # print(line.strip())
                    extrated_line.append(line.strip())
                    count += 1
            print(f"Total Courses in {course}: {count}")
            return extrated_line
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return []
    except Exception as e:
        print(f"The code encountered some problem: {e}")


extract_schedule_text('../data/schedule.txt', 'ENG MGT')