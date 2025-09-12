import streamlit as st
from datetime import date
import requests


API_URL = "http://localhost:8000"



def add_update_tab():
    selected_date=st.date_input("Enter date",date(2024, 8, 1),label_visibility='collapsed')
    response=requests.get(f'{API_URL}/expenses/{selected_date}')
    if response.status_code==200:
        existing_expenses=response.json()
        
       
    else:
        st.error("failed to retrieve existing expenses")
        existing_expenses=[]
    categories=['Food','Shopping','Rent','Entertainment','Other']
    with st.form(key='expense_form'):
        col1,clo2,col3=st.columns(3)
        with col1:
            st.header('Amount')
        
        with clo2:
            st.header('Category')
        
        with col3:
            st.header('Notes')
        
        expenses=[]
        for i in range(5):
            if i < len(existing_expenses):
                amount=existing_expenses[i]['amount']
                category=existing_expenses[i]['category']
                notes=existing_expenses[i]['notes']
            else:
                amount=0.0
                category='Food'
                notes=''

            col1,clo2,col3=st.columns(3)
            with col1:
                amount_input=st.number_input(label='amount',min_value=0.0,step=1.0,value=amount,key=f'amount_{i}',label_visibility='collapsed')
            with clo2:
               category_input= st.selectbox(label='category',options=categories,index=categories.index(category),key=f"category_{i}",label_visibility='collapsed')
            with col3:
                notes_input=st.text_input(label="Notes",value=notes,key=f'notes_{i}',label_visibility='collapsed')

            expenses.append({'amount':amount_input,
                             'category':category_input,
                             'notes':notes_input})
        
        
        submit_button=st.form_submit_button(label='Submit')
        if submit_button:
            filtered_expenses=[expense for expense in expenses if expense['amount']>0]

            requests.post(f'{API_URL}/expenses/{selected_date}',json=filtered_expenses)
            if response.status_code==200:
                st.success("Expenses saved successfully")
            else:
                st.error("Failed to save expenses")