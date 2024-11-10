import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Database connection parameters
DB_NAME = "coordinates_db"
DB_USER = "root"  # replace with your MySQL username if different
DB_PASSWORD = ""  # replace with your MySQL password if set
DB_HOST = "localhost"
DB_PORT = "3306"

# Load CSV files
coordinates_df = pd.read_csv('latitude_longitude_details.csv')
terrain_df = pd.read_csv('terrain_classification.csv')

# Create database engine for MySQL
engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load data into MySQL tables (replace existing tables if they exist)
coordinates_df.to_sql('latitude_longitude_details', engine, if_exists='replace', index=False)
terrain_df.to_sql('terrain_classification', engine, if_exists='replace', index=False)

print("Data successfully loaded into MySQL tables.")

# Database connection parameters for querying
conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=int(DB_PORT)
)

# Create a cursor object
cur = conn.cursor()

# SQL query to select points with terrain 'road' excluding 'civil station'
query = """
    SELECT latitude_longitude_details.latitude, latitude_longitude_details.longitude
    FROM latitude_longitude_details
    JOIN terrain_classification 
    ON latitude_longitude_details.KM = terrain_classification.`distance (in km)`  -- Column with space and parentheses
    WHERE terrain_classification.terrain = 'road' 
    AND terrain_classification.terrain NOT LIKE '%civil station%';
"""

# Execute the query
cur.execute(query)

# Fetch and print all matching points
results = cur.fetchall()
if results:
    for row in results:
        print(row)
else:
    print("No results found matching the criteria.")

# Close the cursor and connection
cur.close()
conn.close()
