#this is a orm based program to create a database and tables in it

#from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pyodbc

# Define your connection string
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-6QOQH3N\SQLEXPRESS;'
    r'DATABASE=db_project;'
    r'UID=sa;'
    r'PWD=houman1380;'
)

# Create a new connection
conn = pyodbc.connect(conn_str)

# Create a new cursor
cursor = conn.cursor()

# Execute a query
cursor.execute("""
    IF NOT EXISTS (select * from sysobjects where name='users')
        CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50),
        fullname VARCHAR(50),
        password VARCHAR(50)
    )
""")
conn.commit()
