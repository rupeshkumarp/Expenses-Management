from analytics_UI import analytics_tab
from add_update_UI import add_update_tab
from Analytics_by_month import analytics_by_month_tab
import streamlit as st


st.title('Expense Tracking System')

tab1,tab2,tab3=st.tabs(['Add/Update','Analytics-by-category','Analytics-by-month'])

with tab1:
    add_update_tab()
    
with tab2:
    analytics_tab()


with tab3:
    analytics_by_month_tab()