import mysql.connector
import configparser
from models import Transaction

config = configparser.ConfigParser()
config.read("config.ini")

class Db:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host=config["DATABASE"]["host"],
            user=config["DATABASE"]["user"],
            password=config["DATABASE"]["password"],
            database=config["DATABASE"]["database"]
        )

    def get_category_from_name(self, category_name):
        mycursor = self.mydb.cursor()
        query = "select id, name from categories where name ='%s'"
        mycursor.execute(query%(category_name))
        result = dict(zip(mycursor.column_names, mycursor.fetchone())) 
        return result

    def save_transaction(self, transaction):
        try:
            mycursor = self.mydb.cursor()
            query = "insert into transactions (`amount`, `date`, `categoryId`, `remarks`) values ('%s', '%s', '%s', '%s')"
            amount = transaction.get_amount()
            date = transaction.get_date()
            categoryId = transaction.get_category().id
            remarks = transaction.get_remarks()
            mycursor.execute(query%(amount, date, categoryId, remarks))
            self.mydb.commit()
            return True
        except Exception:
            return False
    
    def get_all_categories(self):
        mycursor = self.mydb.cursor()
        query = "select * from categories;"
        mycursor.execute(query)
        results = mycursor.fetchall()
        categories = {}
        for result in results:
            categories[result[0]] = {"option": result[1]}
        return categories
    
    def get_months_transactions(self, month, year):
        mycursor = self.mydb.cursor()
        query = "select t.id as Id, t.amount as `Transaction Amount`, c.name as Category, t.date, t.remarks from transactions t left join categories c on t.categoryId = c.id where month(t.date) = %s and year(t.date) = %s;"
        mycursor.execute(query%(month, year))
        resultSet = list(map(lambda result: dict(zip(mycursor.column_names, result)), mycursor.fetchall()))
        return resultSet
