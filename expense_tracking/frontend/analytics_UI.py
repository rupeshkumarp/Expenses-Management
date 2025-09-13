import streamlit as st
from datetime import date
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', date(2024, 8, 1), key='start_date')
    with col2:
        end_date = st.date_input('End Date', date(2024, 8, 5), key='end_date')
    
    if st.button('Get Analytics'):
        payload = {
            "expense_date_from": start_date.strftime('%Y-%m-%d'),
            "expense_date_to": end_date.strftime('%Y-%m-%d')
        }
        try:
            api_response = requests.post(f'{API_URL}/analytics/', json=payload)
            if api_response.status_code != 200:
                st.error("Failed to fetch analytics.")
                return
            response = api_response.json()
            if not response:
                st.info("No data found for the selected range.")
                return
        except Exception as e:
            st.error(f"Error fetching analytics: {e}")
            return

        data = {
            'Category': list(response.keys()),
            "total": [response[category]['total'] for category in response],
            'Percentage': [response[category]['percentage'] for category in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by='total', ascending=False)

        st.title('Expense Breakdown')
        st.bar_chart(df_sorted.set_index('Category')['Percentage'], use_container_width=True)

        df_sorted['total'] = df_sorted["total"].map("{:.2f}".format)
        df_sorted['Percentage'] = df_sorted['Percentage'].map("{:.2f}".format)

        st.table(df_sorted)