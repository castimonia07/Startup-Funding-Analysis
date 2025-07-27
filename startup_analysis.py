import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set the color palette
plt.style.use('default')
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

def load_startup_analysis(df, startup_name):
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .profile-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title with emoji and styling
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🚀 {startup_name}</h1>
        <p style="color: #f8f9fa; margin: 0.5rem 0 0 0;">Comprehensive Startup Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter data for selected startup
    startup_df = df[df['startup'] == startup_name]
    
    if startup_df.empty:
        st.error("❌ No data found for this startup.")
        return
    
    # Key metrics with enhanced styling
    st.markdown('<div class="section-header">📊 Key Performance Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_funding = startup_df['amount'].sum()
        st.metric("💰 Total Funding", f"${total_funding:,.0f}", delta=f"{total_funding/1000000:.1f}M")
    
    with col2:
        total_rounds = startup_df.shape[0]
        st.metric("🔄 Total Rounds", total_rounds, delta=f"{total_rounds} rounds")
    
    with col3:
        latest_valuation = startup_df['amount'].max()
        st.metric("📈 Highest Round", f"${latest_valuation:,.0f}", delta=f"{latest_valuation/1000000:.1f}M")
    
    with col4:
        sectors = startup_df['vertical'].unique()
        st.metric("🏢 Sectors", len(sectors), delta=f"{len(sectors)} vertical(s)")

    # Additional metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_funding = startup_df['amount'].mean()
        st.metric("📊 Avg Round Size", f"${avg_funding:,.0f}", delta=f"{avg_funding/1000000:.1f}M avg")
    
    with col2:
        first_funding = startup_df['year'].min()
        st.metric("🎯 First Funding", int(first_funding), delta=f"Year {int(first_funding)}")
    
    with col3:
        last_funding = startup_df['year'].max()
        st.metric("🕐 Last Funding", int(last_funding), delta=f"Year {int(last_funding)}")
    
    with col4:
        funding_span = last_funding - first_funding + 1
        st.metric("⏱️ Active Years", int(funding_span), delta=f"{int(funding_span)} years")

    # Startup Profile Card with enhanced styling
    st.markdown('<div class="section-header">🏢 Company Profile</div>', unsafe_allow_html=True)
    
    profile_col1, profile_col2 = st.columns(2)
    
    with profile_col1:
        st.markdown(f"""
        <div class="profile-card">
            <h4>📋 Basic Information</h4>
            <p><strong>🏭 Industry:</strong> <span style="color:#274670;">{startup_df['vertical'].iloc[0]}</span></p>
            <p><strong>🏙️ Headquarters:</strong> <span style="color:#274670;">{startup_df['city'].iloc[0]}</span></p>
            <p><strong>🎯 Latest Round:</strong> <span style="color:#274670;">{startup_df.sort_values('date').iloc[-1]['round']}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with profile_col2:
        growth_rate = ((latest_valuation - startup_df['amount'].iloc[0]) / startup_df['amount'].iloc[0] * 100) if len(startup_df) > 1 else 0
        total_investors = len([inv.strip() for investors_str in startup_df['investors'].dropna() for inv in str(investors_str).split(',')])
        
        st.markdown(f"""
        <div class="profile-card">
            <h4>📈 Performance Metrics</h4>
            <p><strong>📊 Growth Rate:</strong> <span style="color:#274670;">{growth_rate:.1f}%</span></p>
            <p><strong>🤝 Total Investors:</strong> <span style="color:#274670;">{total_investors}</span></p>
            <p><strong>💎 Valuation Trend:</strong> <span style="color:#274670;">{'📈 Increasing' if growth_rate > 0 else '📉 Stable'}</span></p>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Funding Growth Analysis
    st.markdown('<div class="section-header">📈 Funding Growth Analysis</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        startup_df_sorted = startup_df.sort_values('date')
        startup_df_sorted['cumulative_funding'] = startup_df_sorted['amount'].cumsum()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(startup_df_sorted['year'], startup_df_sorted['cumulative_funding'], 
                marker='o', linewidth=3, markersize=10, color=colors[0])
        ax.fill_between(startup_df_sorted['year'], startup_df_sorted['cumulative_funding'], 
                       alpha=0.3, color=colors[0])
        ax.set_title("💰 Cumulative Funding Over Time", fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Cumulative Funding ($)", fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        round_funding = startup_df.groupby('round')['amount'].sum().sort_values(ascending=True)
        bars = ax.barh(round_funding.index, round_funding.values, color=colors[:len(round_funding)])
        ax.set_title("🎯 Funding by Round Type", fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel("Funding Amount ($)", fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.0f}', ha='left', va='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

    # Enhanced Investor Network Analysis
    st.markdown('<div class="section-header">🤝 Investor Network</div>', unsafe_allow_html=True)
    
    all_investors = []
    for investors_str in startup_df['investors'].dropna():
        all_investors.extend([inv.strip() for inv in str(investors_str).split(',')])
    
    investor_counts = pd.Series(all_investors).value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top Investors")
        for i, (investor, count) in enumerate(investor_counts.items()):
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {colors[i % len(colors)]}20, {colors[i % len(colors)]}10); 
                        padding: 0.5rem; border-radius: 8px; margin: 0.2rem 0; border-left: 4px solid {colors[i % len(colors)]};">
                <strong>{investor}</strong>: {count} round(s)
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if len(investor_counts) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            wedges, texts, autotexts = ax.pie(investor_counts.values, labels=investor_counts.index, 
                                            autopct='%1.1f%%', colors=colors[:len(investor_counts)])
            ax.set_title("📊 Investor Distribution", fontsize=14, fontweight='bold', pad=20)
            
            # Enhance text styling
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            plt.tight_layout()
            st.pyplot(fig)

    # Enhanced Timeline Analysis
    st.markdown('<div class="section-header">📅 Funding Timeline</div>', unsafe_allow_html=True)
    timeline_df = startup_df.sort_values('date')[['date', 'round', 'amount', 'investors']]
    timeline_df['amount_formatted'] = timeline_df['amount'].apply(lambda x: f"${x:,.0f}")
    
    for index, row in timeline_df.iterrows():
        with st.expander(f"🗓️ {row['date']} - {row['round']} Round - {row['amount_formatted']}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**💰 Amount:** {row['amount_formatted']}")
                st.markdown(f"**🔄 Round:** {row['round']}")
            with col2:
                st.markdown(f"**🤝 Investors:** {row['investors']}")

    # Enhanced Industry Comparison
    st.markdown('<div class="section-header">🏭 Industry Comparison</div>', unsafe_allow_html=True)
    
    industry_data = df[df['vertical'] == startup_df['vertical'].iloc[0]]
    industry_stats = {
        'avg_funding': industry_data['amount'].mean(),
        'median_funding': industry_data['amount'].median(),
        'total_startups': industry_data['startup'].nunique()
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        startup_vs_avg = (total_funding / industry_stats['avg_funding'] - 1) * 100
        delta_color = "normal" if startup_vs_avg > 0 else "inverse"
        st.metric("📊 vs Industry Avg", f"{startup_vs_avg:+.1f}%", 
                 delta=f"{'Above' if startup_vs_avg > 0 else 'Below'} average")
    
    with col2:
        startup_vs_median = (total_funding / industry_stats['median_funding'] - 1) * 100
        st.metric("📈 vs Industry Median", f"{startup_vs_median:+.1f}%",
                 delta=f"{'Above' if startup_vs_median > 0 else 'Below'} median")
    
    with col3:
        industry_funding_totals = industry_data.groupby('startup')['amount'].sum()
        percentile = (industry_funding_totals < total_funding).mean() * 100
        st.metric("🏆 Industry Percentile", f"{percentile:.0f}th",
                 delta=f"Top {100-percentile:.0f}%")

    # Enhanced charts for remaining sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Yearly Funding Trend")
        funding_timeline = startup_df.groupby('year')['amount'].sum()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(funding_timeline.index, funding_timeline.values, marker='o', 
               linewidth=3, markersize=8, color=colors[1])
        ax.fill_between(funding_timeline.index, funding_timeline.values, alpha=0.3, color=colors[1])
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Funding Amount ($)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### 🔄 Round Distribution")
        round_funding = startup_df.groupby('round')['amount'].sum()
        fig, ax = plt.subplots(figsize=(8, 4))
        wedges, texts, autotexts = ax.pie(round_funding.values, labels=round_funding.index, 
                                        autopct='%1.1f%%', colors=colors[:len(round_funding)])
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        plt.tight_layout()
        st.pyplot(fig)

    # Enhanced data table
    st.markdown('<div class="section-header">📋 Investment Details</div>', unsafe_allow_html=True)
    display_df = startup_df[['date', 'round', 'amount', 'investors']].copy()
    display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(display_df, use_container_width=True)

    # Success message
    st.success("✅ Analysis complete! All metrics and visualizations have been generated successfully.")

    