import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Load Data
@st.cache_data # This keeps the app fast by caching the CSV load
def load_data():
    df = pd.read_csv('df_hourly_filtered.csv') 
    # Add your cleaning logic here (summing columns, dates, etc.)
    return df

df = load_data()

# 2. Sidebar Widgets
st.sidebar.title("Filters")
selected_year = st.sidebar.selectbox("Year", df['YEAR'].unique())
selected_zone = st.sidebar.selectbox("Zone", df['Zone'].unique())

# 3. Filter Data
filtered_df = df[
    (df['YEAR'] == selected_year) & 
    (df['Zone'] == selected_zone)
]

dynamic_max = filtered_df['HOURLY_DEMAND'].max()
# Add 10% padding so the bars don't touch the very top of the chart
y_limit = dynamic_max * 1.1
    
# 4. Create Plot
fig = px.bar(
    filtered_df, x='Day_Hour_Label', y='HOURLY_DEMAND', 
    color='Scenarios', barmode='group',
    title=f"Demand for {selected_zone} in Year {selected_year}",
    range_y=[0, y_limit]
)

# 5. Display Plot
st.plotly_chart(fig, use_container_width=True)