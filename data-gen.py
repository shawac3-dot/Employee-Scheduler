import sqlite3
import os
import random

DATABASE = '/nfs/employees.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_data(num_employees):
    db = connect_db()

    for i in range(num_employees):
        employee_id = f'EMP{i:03d}'
        name = f'Test Employee {i}'
        phone = f'555-010-{i:04d}'
        hourly_rate = round(random.uniform(15, 50), 2)

        try:
            db.execute('''
                INSERT INTO employees (employee_id, name, phone, hourly_rate)
                VALUES (?, ?, ?, ?)
            ''', (employee_id, name, phone, hourly_rate))
        except sqlite3.IntegrityError:
            print(f"Skipping {employee_id} — already exists.")
            continue

    db.commit()
    print('Done adding test data.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)
