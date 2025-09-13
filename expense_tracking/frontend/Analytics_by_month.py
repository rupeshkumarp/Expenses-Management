import streamlit as st
from datetime import date
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_by_month_tab():
    st.title('Monthly Expense Summary')

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', date(2024, 8, 1), key='month_start')
    with col2:
        end_date = st.date_input('End Date', date(2024, 9, 1), key='month_end')

    if st.button('Get Monthly Summary'):
        try:
            response = requests.get(
                f"{API_URL}/expenses_by_month/{start_date}/{end_date}"
            )
            if response.status_code != 200:
                st.error("Failed to fetch monthly summary.")
                return
            data = response.json()
            if not data:
                st.info("No data found for the selected range.")
                return
        except Exception as e:
            st.error(f"Error fetching monthly summary: {e}")
            return

        # Convert to DataFrame
        df = pd.DataFrame(data)
        if df.empty:
            st.info("No data to display.")
            return

        # Bar chart
        st.bar_chart(df.set_index('month')['total_amount'], use_container_width=True)

        # Show table
        df['total_amount'] = df['total_amount'].map("{:.2f}".format)
        st.table(df)
    
    