import googlemaps

from dotenv import load_dotenv
import os
import pandas as pd
from pathlib import Path

load_dotenv()
api_keys = os.getenv('GOOGLE_MAP_API_KEY')

def TimeandDistance(coordinates: dict) -> list:

    address = []
    building_name = []

    # make the location and location name as api consistent
    for name, coords in coordinates.items():
        building_name.append(name)
        address.append([coords['lat'], coords['lon']])

    gmaps = googlemaps.Client(key=api_keys)

    allResultsRow = []
    chunkSize = 4
    for i in range(0, len(address), chunkSize):
        originsChunks = address[i : i+chunkSize]
        matrix_result = gmaps.distance_matrix(
            origins=originsChunks,
            destinations=address,
            mode="walking"
        )
        allResultsRow.extend(matrix_result['rows'])

    return allResultsRow

def calculate_matrices(allResultsRow:list, building_name:list):
    distanceMatrix = []
    timeMatrix = []

    for row in allResultsRow:
        distanceRow = []
        timeRow = []

        for element in row['elements']:
            if element['status'] == 'OK':
                distanceRow.append(element['distance']['value'])
                timeRow.append(element['duration']['value'])
            else:
                distanceRow.append(-1)
                timeRow.append(-1)

        distanceMatrix.append(distanceRow)
        timeMatrix.append(timeRow)

    distance_df = pd.DataFrame(distanceMatrix, index=building_name, columns=building_name)
    duration_df = pd.DataFrame(timeMatrix, index=building_name, columns=building_name)

    output_dir = Path("../csv_file")
    output_dir.mkdir(parents=True, exist_ok=True)
    

    distance_df.to_csv(output_dir / "mst_distance_matrix_meters.csv")
    duration_df.to_csv(output_dir / "mst_time_matrix_seconds.csv")

    print("Final Matrices are created!!")
    print(f"CSV files saved to: {output_dir.resolve()}")