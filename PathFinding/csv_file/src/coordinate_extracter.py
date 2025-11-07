from geopy.geocoders import Nominatim
import time
import folium
from pathlib import Path

def geocoding(addresses: list ) -> dict:
    """
    This function will geocode the locations into the lattitude and longitude point.
    """
    geolocator = Nominatim(user_agent="Building_address")

    #Creates a dictionary with longitude and latitude of all the addresses
    coordinates = {}

    name_map = {
        "1400 North Bishop Avenue, Rolla, MO": "V.H. McNutt Hall, Rolla, MO"
    }

    #iterates through every addresses and add their coordinates
    for address in addresses:
        try:

            time.sleep(1)
            location = geolocator.geocode(
                query=address,
                country_codes=["USA"],
            )

            if location:

                display_name = name_map.get(address, address)
                lat = location.latitude
                lon = location.longitude

                coordinates[display_name] = {"lat": lat, "lon": lon}
            else:
                print(f"Issue: Invalid Address/ Address not found for {address}")
                coordinates[address] = None
            
        except Exception as e:
            print(f"An error occured with address '{address}': {e}")
            coordinates[address] = None

    return coordinates

def create_validation_map(coordinates: dict, name: str):
    """
    This function will make sure the coordinate created from this are validated.
    """

    map_center = [37.955086935972474, -91.77311696871674]
    my_map = folium.Map(location=map_center, zoom_start=16)

    for building_name, coords in coordinates.items():
        coordinate = [coords['lat'], coords['lon']]
        folium.Marker(location=coordinate, popup=building_name).add_to(my_map)

    output_dir = Path("./visualization") 
    output_dir.mkdir(parents=True, exist_ok=True)

    save_path = output_dir / name

    my_map.save(save_path)
    print(f"Map validation file saved to: {save_path}")