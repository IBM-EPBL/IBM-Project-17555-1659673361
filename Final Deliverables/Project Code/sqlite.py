import sqlite3 

conn= sqlite3.connect('database.db')
print('opened')

conn.execute('CREATE TABLE user (name TEXT, email TEXT, phone TEXT, password TEXT)')
print("table created")
conn.close()