from analytics_UI import analytics_tab
from add_update_UI import add_update_tab
import streamlit as st


st.title('Expense Tracking System')

tab1,tab2=st.tabs(['Add/Update','Analytics'])

with tab1:
    add_update_tab()
    
with tab2:
    analytics_tab()
    
