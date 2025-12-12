import os
import sqlite3

temp_db = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'users_new.db')
conn = sqlite3.connect(temp_db)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', tables)
conn.close()
