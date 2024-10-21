import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

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

# Create Tabs for Insights
tab1, tab2, tab3, tab4 = st.tabs(["📍 Geographical Distribution", 
                                  "🏢 Ownership & Facility Types", 
                                  "🔧 Infrastructure & Service Provision", 
                                  "📈 Performance & Socioeconomic Analysis"])

# Tab 1: Geographical Distribution & Accessibility
with tab1:
    st.header("Geographical Distribution & Accessibility")
    
    # Map using Folium
    map_center = [data['Latitude'].mean(), data['Longitude'].mean()]
    map = folium.Map(location=map_center, zoom_start=6)
    
    for index, row in data.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], 
                      popup=f"{row['FacilityName']}, {row['Ownership']}").add_to(map)

    # Display the map in Streamlit
    folium_static(map)

    # Summary metrics
    st.subheader("Summary Metrics")
    total_facilities = len(data)
    st.write(f"Total Facilities: **{total_facilities}**")
    region_counts = data['Region'].value_counts()
    st.bar_chart(region_counts)  # Distribution of Healthcare Facilities by Region

    # Regional and District Healthcare Infrastructure (Choropleth)
    choropleth_fig = px.choropleth(data, 
                                    locations='Region', 
                                    locationmode='country names', 
                                    color='Type', 
                                    title='Regional Healthcare Infrastructure')
    st.plotly_chart(choropleth_fig)

    # Urban vs. Rural Distribution (Pie Chart)
    # Urban vs. Rural Distribution
    urban_rural_counts = data['Town'].apply(lambda x: 'Urban' if isinstance(x, str) and 'Urban' in x else 'Rural' if isinstance(x, str) else 'Unknown').value_counts()

    # Plotting the Urban vs. Rural Distribution
    fig_urban_rural = px.pie(names=urban_rural_counts.index, values=urban_rural_counts.values, title="Urban vs Rural Distribution of Facilities")
    st.plotly_chart(fig_urban_rural)


    # Proximity to Health Facilities (Histogram)
    st.subheader("Proximity to Health Facilities")
    st.write("Distribution of distances to the nearest health facility.")
    data['Distance to Nearest Facility'] = data['Latitude'].apply(lambda x: abs(x - map_center[0]))  # Sample calculation
    st.plotly_chart(px.histogram(data, x='Distance to Nearest Facility', nbins=30, 
                                  title='Histogram of Distance to Nearest Facility'))

    # Distance to Nearest Facility (Box Plot)
    st.subheader("Distance to Nearest Facility (Box Plot)")
    st.plotly_chart(px.box(data, x='Type', y='Distance to Nearest Facility', 
                            title='Box Plot of Distance to Nearest Facility by Facility Type'))

    # Healthcare Accessibility by Road Networks (Heatmap)
    st.subheader("Healthcare Accessibility by Road Networks")
    # Sample heatmap (this would require actual road network data)
    st.write("Heatmap placeholder - requires additional data for roads.")
    st.write("Visualizing healthcare accessibility by road networks requires geospatial data.")
    
# Tab 2: Ownership & Facility Types
with tab2:
    st.header("Ownership & Facility Types")
    
    # Facility Type Distribution
    fig = px.pie(data, names='Type', title="Facility Type Distribution")
    st.plotly_chart(fig)

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

# Tab 3: Infrastructure & Service Provision
with tab3:
    st.header("Infrastructure & Service Provision")

    # Specialized Facilities Count
    if 'Specialized Services' in data.columns:
        specialized_facilities = data[data['Specialized Services'] == 'Yes']
        st.write(f"Specialized Facilities Count: **{len(specialized_facilities)}**")
    else:
        st.write("Specialized Services data is missing.")

    # Infrastructure Quality Inference (Bar Chart)
    # Sample bar chart based on a hypothetical column
    if 'Infrastructure Quality' in data.columns:
        infrastructure_quality = data['Infrastructure Quality'].value_counts()
        st.plotly_chart(px.bar(x=infrastructure_quality.index, y=infrastructure_quality.values, 
                                title='Infrastructure Quality Inference'))

    # Healthcare Facility Growth Trends (Time Series)
    st.write("Healthcare Facility Growth Trends Placeholder.")
    st.write("To visualize trends, time series data is required.")

    # Performance and Resource Allocation Recommendations (KPI Dashboard)
    st.write("Performance and Resource Allocation Recommendations Placeholder.")
    st.write("KPI analysis requires defined metrics.")

    # Facility Utilization and Capacity Inference (Heatmap)
    st.write("Facility Utilization and Capacity Inference Heatmap Placeholder.")
    st.write("Requires data on facility usage.")

# Tab 4: Healthcare Performance & Socioeconomic Analysis
with tab4:
    st.header("Healthcare Performance & Socioeconomic Analysis")

    # Correlation between Population and Facilities
    if 'Population' in data.columns:
        fig4 = px.scatter(data, x='Population', y='Number of Facilities', color='Region',
                          title="Correlation between Population & Number of Facilities")
        st.plotly_chart(fig4)
    else:
        st.write("Population data is missing for this analysis.")

    # Regional Leadership in Healthcare Development (Bar Chart)
    st.write("Regional Leadership in Healthcare Development Placeholder.")
    st.write("Requires leadership metrics.")

    # Urban vs. Rural Healthcare Quality (Comparison Chart)
    st.write("Urban vs Rural Healthcare Quality Placeholder.")
    st.write("Requires quality metrics for comparison.")

    # Seasonal or Crisis Preparedness (Line Chart)
    st.write("Seasonal or Crisis Preparedness Placeholder.")
    st.write("Requires historical data on healthcare preparedness.")

# Footer
st.markdown("### Powered by Streamlit")
