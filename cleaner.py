import pandas as pd
import streamlit as st

# Load the dataset
data = pd.read_csv('Health-Sector.csv')

# Display the original dataset
st.title("Healthcare Facilities Dataset Cleaning")
st.write("Original Dataset Preview")
st.dataframe(data)

# Step 1: Check for missing values
missing_values = data.isnull().sum()
st.write("Missing values in each column:")
st.write(missing_values)

# Step 2: Drop rows with missing Latitude or Longitude
data = data.dropna(subset=['Latitude', 'Longitude'])

# Step 3: Drop duplicates
data = data.drop_duplicates()

# Step 4: Trim whitespace from string columns
string_columns = ['Region', 'Ownership', 'FacilityName', 'Type']  # Add other string columns if necessary
for col in string_columns:
    data[col] = data[col].str.strip()

# Step 5: Check and convert data types
data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')  # Convert to float, set errors to NaN
data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')  # Convert to float, set errors to NaN

# Step 6: Drop any rows that resulted in NaN after type conversion
data = data.dropna(subset=['Latitude', 'Longitude'])

# Step 7: (Optional) Check for outliers in numerical columns (e.g., Latitude, Longitude)
# You can define your own criteria for what you consider an outlier
lat_min, lat_max = -90, 90  # Latitude bounds
long_min, long_max = -180, 180  # Longitude bounds
data = data[(data['Latitude'] >= lat_min) & (data['Latitude'] <= lat_max)]
data = data[(data['Longitude'] >= long_min) & (data['Longitude'] <= long_max)]

# Display cleaned dataset
st.write("Cleaned Dataset Preview")
st.dataframe(data)

# Save cleaned dataset if needed
cleaned_file_path = 'Cleaned_Health_Sector.csv'
data.to_csv(cleaned_file_path, index=False)
st.write(f"Cleaned dataset saved as {cleaned_file_path}")
