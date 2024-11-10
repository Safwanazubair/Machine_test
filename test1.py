import pandas as pd
import geopy.distance
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load the CSV files
coordinates_df = pd.read_csv('latitude_longitude_details.csv')
terrain_df = pd.read_csv('terrain_classification.csv')

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# Check and fix discontinuous points
def fix_discontinuous_path(df):
    corrected_coords = [df.iloc[0]]  # Start with the first point
    
    for i in range(1, len(df)):
        prev_point = corrected_coords[-1]
        curr_point = df.iloc[i]
        
        # Calculate the distance between the previous point and the current one
        distance = calculate_distance(prev_point['latitude'], prev_point['longitude'], curr_point['latitude'], curr_point['longitude'])
        
        if distance > 0.1:  # Threshold for discontinuous points (adjust as needed)
            # Optionally, interpolate or skip discontinuous points
            print(f"Discontinuity detected between point {i-1} and point {i}. Fixing...")
            # Here, you could interpolate or just exclude the discontinuous point:
            # For simplicity, I'll just skip the point with a large distance
            continue  # Skip the point with discontinuity
        else:
            corrected_coords.append(curr_point)  # Add the point if it's continuous
    
    return pd.DataFrame(corrected_coords)

# Apply the fix to the coordinates
fixed_coords_df = fix_discontinuous_path(coordinates_df)

# Save the corrected path to a new CSV file
fixed_coords_df.to_csv('fixed_coordinates.csv', index=False)

# Plot before and after
plt.figure(figsize=(10, 6))

# Plot original points
plt.subplot(1, 2, 1)
plt.scatter(coordinates_df['longitude'], coordinates_df['latitude'], color='red', label='Original Path')
plt.title("Original Coordinates")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()

# Plot fixed points
plt.subplot(1, 2, 2)
plt.scatter(fixed_coords_df['longitude'], fixed_coords_df['latitude'], color='green', label='Fixed Path')
plt.title("Fixed Coordinates")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
