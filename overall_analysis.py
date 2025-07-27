import streamlit as st
import matplotlib.pyplot as plt

def load_overall_analysis(df):
    st.title('Overall Analysis')

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total funding amount
        total = round(df['amount'].sum())
        st.metric("Total", str(total), delta=str(round(total - df['amount'].min())))

    with col2:
        # Maximum amount infused in a startup
        max_amount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head()
        st.metric('Max', str(max_amount.max()), delta=str(round(max_amount.max() - max_amount.min())))

    with col3:
        # Average funding amount
        avg_amount = round(df['amount'].mean())
        st.metric("Average", str(avg_amount), delta=str(round(avg_amount - df['amount'].min())))

    with col4:
        # Total funded startups
        total_startups = df['startup'].nunique()    
        st.metric("Number of Unique Startups", total_startups)
    
    # MoM analysis (visually appealing and compact)
    st.subheader("Month on Month Analysis")
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        y_column = 'amount'
        y_label = 'Total Amount'
    else:
        temp_df = df.groupby(['year', 'month'])['startup'].nunique().reset_index()
        y_column = 'startup'
        y_label = 'Number of Startups Funded'

    temp_df['x_axis'] = temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str)
    fig, ax = plt.subplots(figsize=(7, 3))  # Smaller figure size

    ax.plot(temp_df['x_axis'], temp_df[y_column], marker='o', color='#1f77b4', linewidth=2)
    ax.set_xticks(temp_df['x_axis'][::max(1, len(temp_df['x_axis']) // 10)])  # Fewer x-ticks for clarity
    ax.set_xticklabels(temp_df['x_axis'][::max(1, len(temp_df['x_axis']) // 10)], rotation=45, ha='right', fontsize=8)
    ax.set_ylabel(y_label, fontsize=10)
    ax.set_xlabel('Month', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title('Month-on-Month Funding', fontsize=12)
    fig.tight_layout()
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        # Top 5 startups by funding amount (Horizontal Bar Chart)
        st.subheader("Top 5 Startups by Funding Amount")
        if not max_amount.empty:
            fig, ax = plt.subplots()
            ax.barh(max_amount.index[::-1], max_amount.values[::-1], color='skyblue')
            ax.set_xlabel('Funding Amount')
            ax.set_ylabel('Startup')
            ax.set_title('Top 5 Funded Startups')
            st.pyplot(fig)
        else:
            st.write("No data found for this analysis.")

    with col2:
        # Funding amount by year (Line Chart)
        funding_by_year = df.groupby('year')['amount'].sum()
        st.subheader('Funding Amount by Year')
        fig, ax = plt.subplots()
        ax.plot(funding_by_year.index, funding_by_year.values, marker='o', color='orange', linewidth=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('Total Funding')
        ax.set_title('Yearly Funding Trend')
        st.pyplot(fig)
