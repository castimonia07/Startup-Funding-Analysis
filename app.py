import streamlit as st
import pandas as pd
from overall_analysis import load_overall_analysis
from startup_analysis import load_startup_analysis
from investor_analysis import load_investor_details

st.set_page_config(page_title="Startup Funding Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('stratup_cleaned.csv')
    # Convert 'date' column to datetime and extract year
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    # Convert 'date' column to datetime and extract month
    df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.month
    return df

df = load_data()

# Sidebar for navigation
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis(df)
    # btn1= st.sidebar.button('Load Overall Analysis')
    # if btn1:
    #     load_overall_analysis(df)

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    load_startup_analysis(df, selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    load_investor_details(df, selected_investor)

