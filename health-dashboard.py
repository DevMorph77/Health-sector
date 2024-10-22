import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS for styling
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
.header {
    color: #2E86C1;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Load the CSV file
st.title("🏥 Healthcare Facilities Dashboard")
st.write("### Dataset Preview")

# Load dataset
data = pd.read_csv('Cleaned_Health_Sector.csv')
st.dataframe(data)

# Sidebar Filters
st.sidebar.title("Filters")
selected_region = st.sidebar.selectbox("Select Region", data['Region'].unique())
selected_ownership = st.sidebar.multiselect("Select Ownership Type", data['Ownership'].unique())
selected_type = st.sidebar.multiselect("Select Facility Type", data['Type'].unique())

color_map = {
    'Eastern': '#FFFF00',  # Yellow
    'Greater Accra': '#0000FF',  # Blue
    'Western': '#228B22',  # Forest Green
    'Central': '#FFA500',  # Orange
    'Northern': '#800080',  # Purple
    'Ashanti': '#008000',  # Green
    'Volta': '#DC143C',  # Crimson
    'Brong Ahafo': '#4B0082',  # Indigo
    'Upper West': '#FF00FF',  # Magenta
    'Upper East': '#FFBF00',  # Amber
}


# Create a new column for color based on the region
data['Color'] = data['Region'].map(color_map)

# Create Tabs for Insights
tab1, tab2 = st.tabs(["📍 Geographical Distribution", "🏢 Ownership & Facility Types"])

# Tab 1: Geographical Distribution & Accessibility
with tab1:
    st.header("Geographical Distribution & Accessibility")

    # Plotly Scatter Mapbox with region colors
    fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", hover_name="FacilityName",
                            hover_data=["Region", "Ownership"], zoom=6, height=500,
                            color='Color', color_discrete_map=color_map)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Display the map in Streamlit
    st.plotly_chart(fig)

    # Summary metrics
    st.subheader("Summary Metrics")
    total_facilities = len(data)
    st.write(f"Total Facilities: **{total_facilities}**")
    
    # Distribution of Healthcare Facilities by Region
    region_counts = data['Region'].value_counts()
    st.bar_chart(region_counts)

    # Urban vs. Rural Distribution (Pie Chart)
    urban_rural_counts = data['Town'].apply(lambda x: 'Urban' if isinstance(x, str) and 'Urban' in x else 'Rural' if isinstance(x, str) else 'Unknown').value_counts()
    fig_urban_rural = px.pie(names=urban_rural_counts.index, values=urban_rural_counts.values, title="Urban vs Rural Distribution of Facilities")
    st.plotly_chart(fig_urban_rural)

    # Proximity to Health Facilities (Histogram)
    st.subheader("Proximity to Health Facilities")
    st.write("Distribution of distances to the nearest health facility.")
    data['Distance to Nearest Facility'] = data['Latitude'].apply(lambda x: abs(x - data['Latitude'].mean()))  # Sample calculation
    st.plotly_chart(px.histogram(data, x='Distance to Nearest Facility', nbins=30, title='Histogram of Distance to Nearest Facility'))

    # Distance to Nearest Facility (Box Plot)
    st.subheader("Distance to Nearest Facility (Box Plot)")
    st.plotly_chart(px.box(data, x='Type', y='Distance to Nearest Facility', title='Box Plot of Distance to Nearest Facility by Facility Type'))

    # Healthcare Accessibility by Road Networks (Heatmap)
    st.subheader("Healthcare Accessibility by Road Networks")
    st.write("Heatmap placeholder - requires additional data for roads.")
    st.write("Visualizing healthcare accessibility by road networks requires geospatial data.")

# Tab 2: Ownership & Facility Types
with tab2:
    st.header("Ownership & Facility Types")
    
    # Create a grid layout with one row and two columns
    col1, col2 = st.columns(2)

    with col1:
        # Facility Type Distribution
        fig = px.pie(data, names='Type', title="Facility Type Distribution")
        st.plotly_chart(fig)

    with col2:
        # Ownership Distribution
        ownership_chart = data.groupby(['Region', 'Ownership']).size().reset_index(name='Count')
        fig2 = px.bar(ownership_chart, x='Region', y='Count', color='Ownership', title="Ownership Distribution by Region")
        st.plotly_chart(fig2)

    # CHAG vs. Government Facilities (Stacked Bar Chart)
    chag_government = data[data['Ownership'].isin(['CHAG', 'Government'])]
    st.plotly_chart(px.bar(chag_government, x='Type', color='Ownership', title='CHAG vs Government Facilities'))

    # Comparison of Public vs. Private Facilities
    public_private = data[data['Ownership'].isin(['Government', 'Private'])]
    st.plotly_chart(px.bar(public_private, x='Type', color='Ownership', title='Comparison of Public vs Private Facilities'))

    # Role of Faith-Based Healthcare (Area Chart)
    faith_based = data[data['Ownership'] == 'CHAG']
    st.plotly_chart(px.area(faith_based, x='Region', y='FacilityName', title='Role of Faith-Based Healthcare'))

# Footer
st.markdown("### Powered by Streamlit")
