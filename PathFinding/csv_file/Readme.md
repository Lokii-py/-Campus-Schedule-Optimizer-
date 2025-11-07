# MST Campus Pathfinding Data Pipeline 

This project is a data engineering pipeline designed to calculate the walking distance and travel time between all primary academic buildings at the Missouri University of Science and Technology (MST).

The primary goal of this tool is to generate the foundational data required for an academic research project on **university course timetabling optimization**. By providing accurate, real-world travel metrics, this pipeline enables the development of scheduling models that can minimize student travel time and improve the overall campus experience.

## Features

* **Automated Geocoding**: Converts a list of building names into precise geographic coordinates using the Nominatim (OpenStreetMap) API.
* **Real-World Pathfinding**: Calculates actual walking distances and times using the Google Maps Distance Matrix API, not just straight-line distances.
* **API Limit Handling**: Intelligently batches API requests to stay within the free-tier limits of the Google Maps API.
* **Visual Validation**: Generates an interactive HTML map (`mst_map_validation.html`) using Folium to visually confirm that all building coordinates are correct.
* **Configurable**: All settings, including the building list and output directories, are managed in a simple `config.yaml` file.
* **Clean Data Output**: Produces two clean, labeled CSV files containing the final distance and time matrices, ready for use in data analysis or optimization models.

## Setup and Installation
pending