from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class date_Range(BaseModel):
    expense_date_from: date
    expense_date_to: date



@app.get('/expenses/{expense_date}', response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expense_for_day(expense_date)
    if expenses is None:
        raise HTTPException(status_code=404,detail="No data found")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_helper.delete_db_cursor(expense_date)
    for expense in expenses:
        db_helper.insert_db_cursor(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(daterange:date_Range):
    data=db_helper.fetch_expense_summary(daterange.expense_date_from,daterange.expense_date_to)
    if data is None:
        raise HTTPException(status_code=404,detail="No data found")
    
    total=sum([row['total'] for row in data ])
   

    breakdown={}
    for row in data:
        percentage=(row['total']/total)*100 if total>0 else 0
        breakdown[row['category']]={
            'total':row['total'],
            'percentage':percentage
            }
        
    return breakdown
