#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/app/data/atp_users.db')
cursor = conn.cursor()

# Verificar tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables found:', tables)

# Verificar si la tabla users existe
if any('users' in table for table in tables):
    print('Users table exists')
    cursor.execute("SELECT * FROM users LIMIT 5;")
    users = cursor.fetchall()
    print('Sample users:', users)
else:
    print('Users table NOT found')

conn.close()
