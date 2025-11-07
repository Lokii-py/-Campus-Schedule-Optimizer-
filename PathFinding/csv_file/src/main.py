import yaml
import argparse
from pathlib import Path

from coordinate_extracter import geocoding, create_validation_map
from matrix_calculation import TimeandDistance, calculate_matrices
from shortest_cycle import DataPrep, solve

def main(config_file):

    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    building_name = config.get("name")

    distancePath = Path("../csv_file/mst_distance_matrix_meters.csv")
    timePath = Path("../csv_file/mst_time_matrix_seconds.csv")

    if not (distancePath.exists() and timePath.exists()):
        print("CSV files not found. Running data pipeline")
        coordinates = geocoding(building_name)

        create_validation_map(coordinates, "mst_map_validation.html")

        allResultsRow = TimeandDistance(coordinates)

        calculate_matrices(allResultsRow, building_name)

    # Finding the shortest distance between the building without returning to same place twice
    x, y = DataPrep()
    z = solve(x, y)

    a = geocoding(x)
    create_validation_map(a, "ordered_map_validation.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Matrices")

    default_config = Path(__file__).resolve().parents[1]/"config.yaml"

    parser.add_argument(
        "--config",
        type=str,
        default=default_config,
        help="Path to the config file (default: ./config.yaml).",
    )

    args = parser.parse_args()

    main(args.config)
