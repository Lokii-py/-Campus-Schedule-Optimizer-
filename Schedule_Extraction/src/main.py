import argparse
from pathlib import Path
import pandas as pd
from extract import extract_schedule_data

def main(
    filename: Path,
    courseName: str,
):
    """
    This is the entry port to the code.
    It uses the extract_schedule_data to pull out the information required
    """
    all_the_courses = extract_schedule_data(filename, courseName)

    if all_the_courses.empty:
        print(f"No data is extracted.")

    #debug
    # print("DEBUG: Raw DF:")
    # print(all_the_courses.sample(n=6))

    dynamic_filename = f"{courseName.replace(' ', '_')}.csv"

    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    unclean_dir = root_dir/ "result" / "unclean"
    unclean_dir.mkdir(parents=True, exist_ok=True)
    unclean_path = unclean_dir / dynamic_filename

    all_the_courses.to_csv(unclean_path, index=False)
    print("Unclean result is saved to", unclean_path)

    clean_df = all_the_courses[
        (~all_the_courses['Days & Times'].str.contains("Arranged")) &
        (~all_the_courses['Room'].str.contains("Internet"))
    ]

    clean_dir = root_dir / "result" / "clean"
    clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = clean_dir / dynamic_filename

    print("Clean result is saved to", clean_path)
    clean_df.to_csv(clean_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time Schedule")
    
    parser.add_argument(
        "--path",
        type=Path,
        help="path to the file you want to extract the timing schedule(eg. '../data/schedule.txt')"
    )

    parser.add_argument(
        "--courseName",
        type=str,
        help="Name of the course as per the data(eg. ENG MGT)"
    )

    args = parser.parse_args()

    main(
        args.path,
        args.courseName,
    )