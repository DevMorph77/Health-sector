import pandas as pd

# Load the dataset
data = pd.read_csv('Cleaned_Health_Sector.csv')

# Display the initial number of NaN values in the 'Town' column
print("Initial NaN values in 'Town' column:", data['Town'].isna().sum())

# Replace NaN values in the 'Town' column with 'Unknown'
data['Town'] = data['Town'].fillna('Unknown')

# Display the updated number of NaN values in the 'Town' column
print("NaN values in 'Town' column after replacement:", data['Town'].isna().sum())

# Optionally, save the cleaned DataFrame back to a new CSV file
data.to_csv('Cleaned_Health_Sector_Fixed.csv', index=False)
