import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Startup Funding Analysis", layout="wide")

df=pd.read_csv('stratup_cleaned.csv')

# Convert 'date' column to datetime and extract year
df['year']=pd.to_datetime(df['date'],errors='coerce').dt.year

# Convert 'date' column to datetime and extract month
df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.month

st.sidebar.title('Startup Funding Analysis')
# data cleaning
# df['Investors Name']=df['Investors Name'].fillna('Undisclosed')

# Overall Analysis
def load_overall_analysis():
    st.title('Overall Analysis')

    col1,col2,col3, col4 = st.columns(4)
    with col1:
        # Total funding amount
        total=round(df['amount'].sum())
        st.metric("Total", str(total), delta=str(round(total - df['amount'].min())))

    with col2:
        # Maximum amount infused in a startup
        max_amount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head()
        st.metric('Max',str(max_amount.max()), delta=str(round(max_amount.max() - max_amount.min())))

    with col3:
        #average funding amount
        avg_amount = round(df['amount'].mean())
        st.metric("Average", str(avg_amount), delta=str(round(avg_amount - df['amount'].min())))

    with col4:
        # total funded startups
        total_startups = df['startup'].nunique()    
        st.metric("Number of Unique Startups", total_startups)
    
    # MoM analysis
    st.subheader("Month on Month Analysis")
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
        y_column = 'amount'
        y_label = 'Total Amount'
    else:
        # Count of startups funded each month
        temp_df = df.groupby(['year','month'])['startup'].nunique().reset_index()
        y_column = 'startup'
        y_label = 'Number of Startups Funded'
    
    temp_df['x_axis']= temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str)
    fig, ax = plt.subplots()
    ax.plot(temp_df['x_axis'], temp_df[y_column], marker='o')
    ax.set_xticks(temp_df['x_axis'])
    ax.set_ylabel(y_label)
    st.pyplot(fig)


    # Top 5 startups by funding amount
    st.subheader("Top 5 Startups by Funding Amount")
    if not max_amount.empty:
        fig, ax = plt.subplots()
        ax.bar(max_amount.index, max_amount.values)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("No data found for this analysis.")


    # Funding amount by year
    funding_by_year = df.groupby('year')['amount'].sum()
    st.subheader('Funding Amount by Year')
    fig, ax = plt.subplots()
    ax.bar(funding_by_year.index, funding_by_year.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def load_investor_details(investor):
    st.title(f"Details for Investor: {investor}")
    
    # load the recent 5 investments of the investor
    last5_df=df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','investors','round','amount']]
    st.subheader("Most Recent Investments")
    if not last5_df.empty:
        st.dataframe(last5_df)
    else:
        st.write("No data found for this investor.")

    col1, col2 = st.columns(2)
    with col1:
        # Biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()

        st.subheader("Biggest Investment")
        if not big_series.empty:
            fig, ax = plt.subplots()
            ax.bar(big_series.index,big_series.values)
            st.pyplot(fig)
        else:
            st.write("No data found for this investor.")
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sector Invested In')
        fig, ax = plt.subplots()
        ax.pie(vertical_series.values, labels=vertical_series.index, autopct='%1.1f%%')
        st.pyplot(fig)


    col1, col2 = st.columns(2)

    # Sector-wise analysis
    with col1:
        round_series=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Sector-wise Analysis')
        fig, ax = plt.subplots()
        ax.pie(round_series.values, labels=round_series.index, autopct='%1.1f%%')
        st.pyplot(fig)

    with col2:
        city_series=df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('City-wise Analysis')
        fig, ax = plt.subplots()
        ax.pie(city_series.values, labels=city_series.index, autopct='%1.1f%%')
        st.pyplot(fig)

    
    # Year-wise analysis
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('Year-wise Analysis')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values, marker='o')
    st.pyplot(fig2)

# Sidebar for navigation
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])


if option=='Overall Analysis':
    load_overall_analysis()
    # btn0= st.sidebar.button('Show Overall Analysis')
    # if btn0:
    #     load_overall_analysis()

elif option=='StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    bt1=st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    bt2 = st.sidebar.button('Find Investor Details')
    if bt2:
        load_investor_details(selected_investor)
    # st.title('Investor Analysis')

