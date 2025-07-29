# Indian Kids Screen Time Analytics Dashboard
# Streamlit Application

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Indian Kids Screen Time Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    """Load the dataset"""
    try:
        data = pd.read_csv('indian_kids_screen_time.csv')
        return data
    except FileNotFoundError:
        st.error("Dataset file 'indian_kids_screen_time.csv' not found. Please upload the file.")
        return None

# Data analysis functions
def get_health_risk_analysis(data):
    """Analyze health risks based on screen time"""
    # Define risk categories based on screen time (hours per day)
    def categorize_risk(screen_time):
        if screen_time < 2:
            return "Low Risk"
        elif screen_time < 4:
            return "Moderate Risk" 
        elif screen_time < 6:
            return "High Risk"
        else:
            return "Very High Risk"
    
    data['Risk_Category'] = data['Daily_Screen_Time'].apply(categorize_risk)
    return data

def main():
    # Title and description
    st.title("📱 Indian Kids Screen Time Analytics Dashboard")
    st.markdown("**Analyze screen time patterns and health impacts among Indian children**")
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    # Add risk analysis
    data = get_health_risk_analysis(data)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Age filter
    age_range = st.sidebar.slider(
        "Select Age Range", 
        min_value=int(data['Age'].min()), 
        max_value=int(data['Age'].max()), 
        value=(int(data['Age'].min()), int(data['Age'].max()))
    )
    
    # Gender filter
    gender_options = ['All'] + list(data['Gender'].unique())
    selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
    
    # City type filter
    city_options = ['All'] + list(data['City_Type'].unique())
    selected_city = st.sidebar.selectbox("Select City Type", city_options)
    
    # Device type filter
    device_options = ['All'] + list(data['Device_Type'].unique())
    selected_device = st.sidebar.selectbox("Select Device Type", device_options)
    
    # Apply filters
    filtered_data = data[
        (data['Age'] >= age_range[0]) & 
        (data['Age'] <= age_range[1])
    ]
    
    if selected_gender != 'All':
        filtered_data = filtered_data[filtered_data['Gender'] == selected_gender]
    
    if selected_city != 'All':
        filtered_data = filtered_data[filtered_data['City_Type'] == selected_city]
        
    if selected_device != 'All':
        filtered_data = filtered_data[filtered_data['Device_Type'] == selected_device]
    
    # Key Metrics Row
    st.header("📊 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_screen_time = filtered_data['Daily_Screen_Time'].mean()
        st.metric("Avg Daily Screen Time", f"{avg_screen_time:.2f} hrs")
    
    with col2:
        health_issues_pct = (filtered_data['Reported_Health_Issues'] == 'Yes').mean() * 100
        st.metric("Health Issues %", f"{health_issues_pct:.1f}%")
    
    with col3:
        avg_sleep = filtered_data['Sleep_Hours'].mean()
        st.metric("Avg Sleep Hours", f"{avg_sleep:.1f} hrs")
    
    with col4:
        avg_outdoor = filtered_data['Outdoor_Activity'].mean()
        st.metric("Avg Outdoor Activity", f"{avg_outdoor:.1f} hrs")
    
    with col5:
        high_risk_pct = (filtered_data['Risk_Category'].isin(['High Risk', 'Very High Risk'])).mean() * 100
        st.metric("High Risk Children %", f"{high_risk_pct:.1f}%")
    
    # Charts Row 1
    st.header("📈 Screen Time Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Screen time by age
        age_screen_time = filtered_data.groupby('Age')['Daily_Screen_Time'].mean().reset_index()
        fig1 = px.bar(age_screen_time, x='Age', y='Daily_Screen_Time', 
                     title="Average Screen Time by Age",
                     color='Daily_Screen_Time',
                     color_continuous_scale='Reds')
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Screen time by device type
        device_data = filtered_data.groupby('Device_Type')['Daily_Screen_Time'].mean().reset_index()
        fig2 = px.pie(device_data, values='Daily_Screen_Time', names='Device_Type',
                     title="Screen Time Distribution by Device")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Purpose analysis
        purpose_data = filtered_data['Purpose'].value_counts().reset_index()
        purpose_data.columns = ['Purpose', 'Count']
        fig3 = px.bar(purpose_data, x='Purpose', y='Count',
                     title="Screen Time Purpose Distribution",
                     color='Count',
                     color_continuous_scale='Blues')
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Risk category distribution
        risk_data = filtered_data['Risk_Category'].value_counts().reset_index()
        risk_data.columns = ['Risk_Category', 'Count']
        colors = {'Low Risk': 'green', 'Moderate Risk': 'yellow', 'High Risk': 'orange', 'Very High Risk': 'red'}
        fig4 = px.bar(risk_data, x='Risk_Category', y='Count',
                     title="Health Risk Distribution",
                     color='Risk_Category',
                     color_discrete_map=colors)
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Health Impact Analysis
    st.header("🏥 Health Impact Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Sleep vs Screen Time
        fig5 = px.scatter(filtered_data, x='Daily_Screen_Time', y='Sleep_Hours',
                         color='Reported_Health_Issues',
                         title="Sleep Hours vs Screen Time",
                         trendline="ols")
        fig5.update_layout(height=400)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Academic Performance vs Screen Time
        perf_screen = filtered_data.groupby('Academic_Performance')['Daily_Screen_Time'].mean().reset_index()
        fig6 = px.bar(perf_screen, x='Academic_Performance', y='Daily_Screen_Time',
                     title="Academic Performance vs Average Screen Time",
                     color='Daily_Screen_Time',
                     color_continuous_scale='RdYlBu_r')
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)
    
    # Detailed Analysis Section
    st.header("🔍 Detailed Analysis")
    
    # Health Issues Analysis
    if st.checkbox("Show Health Issues Analysis"):
        health_analysis = filtered_data[filtered_data['Reported_Health_Issues'] == 'Yes']
        
        if len(health_analysis) > 0:
            st.subheader("Children with Reported Health Issues")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Count", len(health_analysis))
            with col2:
                st.metric("Avg Screen Time", f"{health_analysis['Daily_Screen_Time'].mean():.2f} hrs")
            with col3:
                st.metric("Avg Sleep", f"{health_analysis['Sleep_Hours'].mean():.1f} hrs")
            
            # Show health issues by various factors
            fig7 = px.histogram(health_analysis, x='Age', title="Age Distribution of Children with Health Issues")
            st.plotly_chart(fig7, use_container_width=True)
            
            fig8 = px.histogram(health_analysis, x='Device_Type', title="Device Usage of Children with Health Issues")
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.info("No health issues reported in the filtered data.")
    
    # Recommendations Section
    st.header("💡 Recommendations")
    
    # Calculate key insights
    high_screen_time_kids = len(filtered_data[filtered_data['Daily_Screen_Time'] > 6])
    low_sleep_kids = len(filtered_data[filtered_data['Sleep_Hours'] < 7])
    low_outdoor_kids = len(filtered_data[filtered_data['Outdoor_Activity'] < 1])
    
    recommendations = []
    
    if high_screen_time_kids > 0:
        recommendations.append(f"🚨 {high_screen_time_kids} children have excessive screen time (>6 hours/day). Consider implementing screen time limits.")
    
    if low_sleep_kids > 0:
        recommendations.append(f"😴 {low_sleep_kids} children are getting insufficient sleep (<7 hours). Promote better sleep hygiene.")
    
    if low_outdoor_kids > 0:
        recommendations.append(f"🌳 {low_outdoor_kids} children have minimal outdoor activity (<1 hour). Encourage more physical activities.")
    
    if health_issues_pct > 5:
        recommendations.append(f"⚠️ {health_issues_pct:.1f}% of children report health issues. Consider wellness programs.")
    
    for rec in recommendations:
        st.write(rec)
    
    # Data Export
    st.header("📥 Export Data")
    if st.button("Download Filtered Data as CSV"):
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"filtered_screen_time_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()