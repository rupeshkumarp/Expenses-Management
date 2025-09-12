from backend import db_helper


def test_fetch_expense_for_day():
     expenses=db_helper.fetch_expense_for_day("2024-08-15")

     assert len(expenses)==1
     assert expenses[0]['amount']==10.0
     assert expenses[0]['category']=='Shopping'
     assert expenses[0]['notes']=='Bought potatoes'

def test_fetch_expense_for_category():
     expenses=db_helper.fetch_expense_for_category("2024-08-01",'2024-08-05')

     assert expenses[0]['sum(amount)']==225
     assert expenses[1]['category']=='Shopping'
def test_fetch_particular_category():
     expenses=db_helper.fetch_particular_category('Food')

     assert len(expenses)==17
     assert expenses[0]['amount']==100
     assert expenses[0]['notes']=='Dinner at a restaurant'
