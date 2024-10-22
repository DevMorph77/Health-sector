import streamlit as st
import pandas as pd
import plotly.express as px
import xlsxwriter

# Load the dataset
data = pd.read_csv('Cleaned_Health_Sector.csv')

# Sidebar Filters
selected_region = st.sidebar.selectbox("Select Region", data['Region'].unique())
selected_ownership = st.sidebar.multiselect("Select Ownership Type", data['Ownership'].unique())
selected_type = st.sidebar.multiselect("Select Facility Type", data['Type'].unique())

# Filtered Data
filtered_data = data[(data['Region'] == selected_region) &
                     (data['Ownership'].isin(selected_ownership)) &
                     (data['Type'].isin(selected_type))]

# Write the filtered data and relevant statistics to Excel
excel_file = 'Healthcare_Facilities_Report.xlsx'
with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    # Write raw data
    data.to_excel(writer, sheet_name='Raw Data', index=False)
    
    # Total Facilities by Region
    region_counts = data['Region'].value_counts()
    region_counts.to_excel(writer, sheet_name='Region Stats')
    
    # Ownership Distribution
    ownership_chart = data.groupby(['Region', 'Ownership']).size().reset_index(name='Count')
    ownership_chart.to_excel(writer, sheet_name='Ownership Distribution', index=False)
    
    # Facility Type Distribution
    facility_type_dist = data['Type'].value_counts()
    facility_type_dist.to_excel(writer, sheet_name='Facility Type Distribution')

    # Proximity to Health Facilities
    data['Distance to Nearest Facility'] = data['Latitude'].apply(lambda x: abs(x - data['Latitude'].mean()))  # Simplified sample calculation
    data[['FacilityName', 'Distance to Nearest Facility']].to_excel(writer, sheet_name='Distance to Facilities', index=False)
    
    # Create a simple bar chart for Region Stats
    workbook = writer.book
    worksheet = writer.sheets['Region Stats']
    chart = workbook.add_chart({'type': 'bar'})
    
    chart.add_series({
        'categories': ['Region Stats', 1, 0, len(region_counts), 0],
        'values':     ['Region Stats', 1, 1, len(region_counts), 1],
        'name':       'Facilities by Region',
    })
    
    chart.set_title({'name': 'Facilities by Region'})
    chart.set_x_axis({'name': 'Region'})
    chart.set_y_axis({'name': 'Number of Facilities'})
    worksheet.insert_chart('D2', chart)

    # Add charts for Ownership and Facility Type distribution
    worksheet2 = writer.sheets['Ownership Distribution']
    chart2 = workbook.add_chart({'type': 'column'})
    chart2.add_series({
        'categories': ['Ownership Distribution', 1, 0, len(ownership_chart), 0],
        'values': ['Ownership Distribution', 1, 2, len(ownership_chart), 2],
        'name': 'Ownership Count',
    })
    chart2.set_title({'name': 'Ownership Distribution by Region'})
    worksheet2.insert_chart('E2', chart2)

    worksheet3 = writer.sheets['Facility Type Distribution']
    chart3 = workbook.add_chart({'type': 'pie'})
    chart3.add_series({
        'categories': ['Facility Type Distribution', 1, 0, len(facility_type_dist), 0],
        'values': ['Facility Type Distribution', 1, 1, len(facility_type_dist), 1],
    })
    chart3.set_title({'name': 'Facility Type Distribution'})
    worksheet3.insert_chart('E2', chart3)

# Provide a download button for the Excel file in Streamlit
with open(excel_file, 'rb') as f:
    st.download_button('Download Excel Report', f, file_name=excel_file)
