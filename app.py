import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# 1. Load Data
@st.cache_data # This keeps the app fast by caching the CSV load
def load_data_from_gdrive(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    df = pd.read_csv(url)
    
    return df

GOOGLE_DRIVE_FILE_ID = "1IWn9IAai4Q5dwN72HU7dVATisH_8F2Ta"

df = load_data_from_gdrive(GOOGLE_DRIVE_FILE_ID)
print(df.info())

unique_zones = df['Zone'].unique()
reordered_zones = ['TOTAL'] + [zone for zone in unique_zones if zone != 'TOTAL']

# 2. Sidebar Widgets
st.sidebar.title("Filters")
selected_year = st.sidebar.selectbox("Year", df['YEAR'].unique())
selected_sector = st.sidebar.selectbox("Year", df['Sector'].unique())
selected_zone = st.sidebar.selectbox("Zone", reordered_zones)

# 3. Filter Data
filtered_df = df[
    (df['YEAR'] == selected_year) & 
    (df['Zone'] == selected_zone) & 
    (df['Sector'] == selected_sector)
]

dynamic_max = filtered_df['HOURLY_DEMAND'].max()
# Add 10% padding so the bars don't touch the very top of the chart
y_limit = dynamic_max * 1.1
    
# 4. Create Plot
fig = px.bar(
    filtered_df, x='Day_Hour_Label', y='HOURLY_DEMAND', 
    color='Scenarios', barmode='group',
    title=f"Demand for {selected_zone} in {selected_sector} Sector in Year {selected_year}",
    range_y=[0, y_limit]
)

fig.update_layout(height=800)

# 5. Display Plot
st.plotly_chart(fig, width='stretch')
