import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.set_page_config(layout="wide")

# 1. Load Data
@st.cache_data # This keeps the app fast by caching the CSV load
def load_data_from_gdrive(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    df = pd.read_csv(url)
    
    return df

def load_large_data_from_gdrive(file_id):
    # Construct the base Google Drive URL
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    # Define a temporary local filename to save the download
    output_filename = 'temp_download.csv'
    
    # gdown automatically handles the virus scan warning and downloads the file
    gdown.download(url, output_filename, quiet=False)
    
    # Read the properly downloaded CSV into pandas
    df = pd.read_csv(output_filename)
    
    # Optional: Clean up the downloaded file if you don't want to keep it locally
    if os.path.exists(output_filename):
        os.remove(output_filename)
        
    return df

# 2. Sidebar Widgets
st.sidebar.title("Filters")
selected_analysis = st.sidebar.selectbox("Analysis", ['Pct Chg', 'Demand'])

if selected_analysis == 'Pct Chg':
    GOOGLE_DRIVE_FILE_ID = "1SAe0dahXkriO6u76K4NGQfhxEl4UnpFj"
    chart_title = f"Pct Change for {selected_zone} in {selected_sector} Sector in Year {selected_year} relative to the Growth Scenario"
    yData = 'Percent_Change'
    yaxisTitle = '%'
else:
    GOOGLE_DRIVE_FILE_ID = "1IWn9IAai4Q5dwN72HU7dVATisH_8F2Ta"
    chart_title = f"Demand for {selected_zone} in {selected_sector} Sector in Year {selected_year}"
    yData = 'HOURLY_DEMAND'
    yaxisTitle = 'm3/year'

df = load_large_data_from_gdrive(GOOGLE_DRIVE_FILE_ID)

unique_zones = df['Zone'].unique()
reordered_zones = ['TOTAL'] + [zone for zone in unique_zones if zone != 'TOTAL']

selected_year = st.sidebar.selectbox("Year", df['YEAR'].unique())
selected_sector = st.sidebar.selectbox("Year", df['Sector'].unique())
selected_zone = st.sidebar.selectbox("Zone", reordered_zones)


# 3. Filter Data
filtered_df = df[
    (df['YEAR'] == selected_year) & 
    (df['Zone'] == selected_zone) & 
    (df['Sector'] == selected_sector)
]

dynamic_max = filtered_df[yData].max()

# Add 10% padding so the bars don't touch the very top of the chart
y_limit = dynamic_max * 1.1
    
# 4. Create Plot
fig = px.bar(
    filtered_df, x='Day_Hour_Label', y=yData, 
    color='Scenarios', barmode='group',
    title=f"Demand for {selected_zone} in {selected_sector} Sector in Year {selected_year}",
    range_y=[0, y_limit]
)

fig.update_layout(height=800, yaxis_title=yaxisTitle)

# 5. Display Plot
st.plotly_chart(fig, use_container_width=True)