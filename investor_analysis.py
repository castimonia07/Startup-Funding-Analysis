import streamlit as st
import matplotlib.pyplot as plt

def load_investor_details(df, investor):
    st.title(f"Details for Investor: {investor}")
    
    # Load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor, na=False)].head()[['date','startup','vertical','city','investors','round','amount']]
    
    st.subheader("Most Recent Investments")
    if not last5_df.empty:
        st.dataframe(last5_df)
    else:
        st.write("No data found for this investor.")
        return

    col1, col2 = st.columns(2)
    
    with col1:
        # Biggest investment
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()

        st.subheader("Biggest Investment")
        if not big_series.empty:
            fig, ax = plt.subplots()
            ax.bar(big_series.index, big_series.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.write("No data found for this investor.")
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()

        st.subheader('Sector Invested In')
        if not vertical_series.empty:
            fig, ax = plt.subplots()
            ax.pie(vertical_series.values, labels=vertical_series.index, autopct='%1.1f%%')
            st.pyplot(fig)

    col1, col2 = st.columns(2)

    # Round-wise analysis
    with col1:
        round_series = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()

        st.subheader('Round-wise Analysis')
        if not round_series.empty:
            fig, ax = plt.subplots()
            ax.pie(round_series.values, labels=round_series.index, autopct='%1.1f%%')
            st.pyplot(fig)

    with col2:
        city_series = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()

        st.subheader('City-wise Analysis')
        if not city_series.empty:
            fig, ax = plt.subplots()
            ax.pie(city_series.values, labels=city_series.index, autopct='%1.1f%%')
            st.pyplot(fig)
    
    # Year-wise analysis
    year_series = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()

    st.subheader('Year-wise Analysis')
    if not year_series.empty:
        import plotly.graph_objects as go
        fig2 = go.Figure(data=go.Scatter(x=year_series.index, y=year_series.values, mode='lines+markers'))
        st.plotly_chart(fig2)