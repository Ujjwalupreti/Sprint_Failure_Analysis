import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

class DataBaseConn:
    def __init__(self):
        self.url = URL.create(
            "mysql+mysqlconnector",
            username="root",
            password="Ujjwalsql@2500",
            host="localhost",
            port=3306,
            database="Sprint"
        )

        self.engine = create_engine(self.url)
        
        # self.engine = create_engine("mysql+mysqlconnector://root:Ujjwalsql%402500@localhost/Sprint")

db = DataBaseConn()

data = pd.read_csv("dummy_data.csv")

data.to_sql(
    name="sprint_report",
    con=db.engine,
    if_exists="replace",
    index=False
)

print("Data inserting is done in the database")