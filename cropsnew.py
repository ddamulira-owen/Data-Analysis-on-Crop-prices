import requests
import pandas as pd

# Defining the API endpoint
api_url = "http://quickstats.nass.usda.gov/api/api_GET/"

# Defining the years range for the requests
years = range(2020, 2024)  # Example range: 2020 to 2023

# Initializing a list to store the DataFrames
all_data = []

for year in years:
    params = {
        "key": "59B315D9-DFD8-32BD-B022-4997FCB3CB86",  # My USDA API key
        "source_desc": "SURVEY",
        "sector_desc": "CROPS",
        "commodity_desc": "CORN",
        "year": year,
        "format": "json"
    }
    
    # Make the API request
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Convert the data into a DataFrame
        df = pd.DataFrame(data['data'])
        
        # Select specific columns
        columns = ['year', 'state_name', 'county_name', 'country_code', 'commodity_desc', 'class_desc', 
                   'unit_desc', 'freq_desc', 'group_desc' ,'source_desc', 'sector_desc','commodity_desc',  'statisticcat_desc','begin_code', 'Value']
        df = df[columns]
        
        # Append the DataFrame to the list
        all_data.append(df)
    else:
        print(f"Error for year {year}: {response.status_code}, {response.text}")

# Concatenate all DataFrames in the list into a single DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# Sample 100 rows from the combined data
sampled_data = combined_data.sample(n=200, random_state=1)

# Save the sampled DataFrame to a CSV file
sampled_data.to_csv('crop_prices.csv', index=False)
print("Data saved to crop_prices.csv")
