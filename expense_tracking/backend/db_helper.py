# CURD file  c=create r=retrieve u=update d=delete
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)

    yield cursor
    if commit:
            connection.commit()
    cursor.close()
    connection.close()

def delete_db_cursor(expense_date):
    logger.info(f"delete_db_cursor called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute('delete from expenses where expense_date=%s',(expense_date,))


def insert_db_cursor(expense_date,amount,category,notes):
    logger.info(
        f"insert_db_cursor called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "insert into expenses (expense_date,amount,category,notes) values (%s,%s,%s,%s)"
            ,(expense_date,amount,category,notes)
        )



def fetch_expense_for_day(expense_date):
    logger.info(f"fetch_expenses_for_day called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("select * from expenses where expense_date=%s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def fetch_expense_summary(expense_date_from,expense_date_to):
    logger.info(f"fetch_expense_fro_category called with start: {expense_date_from } end: {expense_date_to}")
    with get_db_cursor() as cursor:
        cursor.execute('select category,sum(amount) as total from expenses where expense_date between %s and %s group by category',
                       (expense_date_from,expense_date_to,))
        expenses = cursor.fetchall()
        return expenses


def fetch_particular_category(category):
    logger.info(f"fetch_particular_category called with {category}")
    with get_db_cursor() as cursor:
        cursor.execute('select * from expenses where category=%s',(category,))
        expenses = cursor.fetchall()
        return expenses


# if __name__ == '__main__':
    # delete_db_cursor(expense_date=('2023-08-23'))
    # fet=fetch_expense_summary('2024-08-01','2024-08-05')
 
    # insert_db_cursor('2023-08-23',500,'Food','Miscellaneous')
    # expenses= fetch_expense_for_day("2024-08-05")
    # for expense in expenses:
    #     print(expense)
    # ex=fetch_particular_category("Food")
    # for expense in ex:
    #     print(expense)