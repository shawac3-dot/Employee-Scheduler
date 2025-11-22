import sqlite3
import os
import random

DATABASE = '/nfs/employees.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_employees):
    """Generate test data for the employees table."""
    db = connect_db()
    for i in range(num_employees):
        employee_id = f'EMP{i:03d}'
        name = f'Test Employee {i}'
        phone = f'555-010-{i:04d}'
        hourly_rate = round(random.uniform(15, 50), 2)  # random rate between $15-$50
        db.execute('''
            INSERT INTO employees (employee_id, name, phone, hourly_rate)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, name, phone, hourly_rate))
    db.commit()
    print(f'{num_employees} test employees added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test employees
