import requests  
import pandas as pd  

# Defining the URL for the earthquake API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?"

# Defining the parameters for the API request
params_dict = {
    "format": "geojson",  # Request data in GeoJSON format
    "starttime": "2018-01-01",  # Start date for the data
    "endtime": "2023-12-31",  # End date for the data
}

# List of alert levels to query
alert_levels = ["green", "yellow", "orange", "red"]

# Initializing an empty list to store data for each alert level
all_earthquake_data = []

for alert_level in alert_levels:
    
    # Updating the alert level in the parameters dictionary
    params_dict["alertlevel"] = alert_level
    
    # Making the GET request to the API with the specified parameters
    response = requests.get(url, params=params_dict)
    
    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        # Parsing the response JSON content into a Python dictionary
        data = response.json()
        
        # Extracting the list of earthquake events from the 'features' key
        features = data['features']
        
        # Looping through each feature (earthquake event) in the features list
        for feature in features:
            
            # Extracting the properties of the earthquake event
            properties = feature['properties']
            
            # Appending the relevant properties to the all_earthquake_data list as a dictionary
            all_earthquake_data.append({
                'time': properties['time'],  # The time of the earthquake
                'place': properties['place'],  # The location of the earthquake
                'mag': properties['mag'],  # The magnitude of the earthquake
                'alert': properties['alert'],  # The alert level
                'status': properties['status'],  # The status of the earthquake report
                'tsunami': properties['tsunami'],  # Tsunami warning (1 if there was a warning, 0 if not)
                'sig': properties['sig'],  # Significance of the earthquake
                'net': properties['net'],  # Network identifier
                'code': properties['code'],  # Event code
                'ids': properties['ids'],  # List of event IDs
                'sources': properties['sources'],  # Data source
                'types': properties['types'],  # Type of seismic event
                'nst': properties['nst'],  # Number of stations that reported the event
                'dmin': properties['dmin'],  # Minimum distance to the nearest station
                'rms': properties['rms'],  # Root mean square of the travel time residuals
                'gap': properties['gap'],  # Azimuthal gap
                'magType': properties['magType'],  # Type of magnitude reported
                'type': properties['type']  # Type of event
            })
    else:
        # Printing an error message if the request was not successful
        print(f"Error: Unable to fetch data for alert level {alert_level}, status code: {response.status_code}")

# Converting the list of dictionaries into a DataFrame
df = pd.DataFrame(all_earthquake_data)

# Printing the DataFrame to display the earthquake data
print(df)

# Using str.extract to split the 'place' column into 'city' and 'country'
df[['city', 'country']] = df['place'].str.extract(r'of\s+(.*?)\,\s+(.*)')

# Converting the 'time' column from Unix timestamp to datetime
df['time'] = pd.to_datetime(df['time'], unit='ms')

# Extracting the month number and the year of each earthquake
df['year'] = df["time"].dt.year
df['monthno'] = df["time"].dt.month

# Month abbreviation using pandas' map method
month_abbrev = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
df['monthabbrev'] = df['monthno'].map(month_abbrev)

# Exporting the xls file for the power bi
df.to_excel("earthquakes_data.xlsx", index=False)

