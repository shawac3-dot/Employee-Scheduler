from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import sqlite3
import os
import math
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DATABASE = '/nfs/employees.db'
PER_PAGE_DEFAULT = 10

# ----------------------------
# Database functions
# ----------------------------
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        # Employees table
        db.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                phone TEXT,
                hourly_rate REAL NOT NULL,
                total_hours REAL DEFAULT 0
            );
        ''')
        # Time logs
        db.execute('''
            CREATE TABLE IF NOT EXISTS time_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                clock_in TEXT,
                clock_out TEXT,
                hours_worked REAL,
                FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
            );
        ''')
        # Schedules
        db.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
            );
        ''')
        db.commit()
        db.close()

# ----------------------------
# Flask Routes
# ----------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        # Delete employee
        if action == 'delete':
            emp_id = request.form.get('id')
            if emp_id:
                db = get_db()
                # Get employee_id string for time_logs
                emp_row = db.execute('SELECT employee_id FROM employees WHERE id=?', (emp_id,)).fetchone()
                if emp_row:
                    employee_id_str = emp_row['employee_id']
                    db.execute('DELETE FROM employees WHERE id=?', (emp_id,))
                    db.execute('DELETE FROM time_logs WHERE employee_id=?', (employee_id_str,))
                    db.execute('DELETE FROM schedules WHERE employee_id=?', (employee_id_str,))
                    db.commit()
                    db.close()
                    flash('Employee deleted successfully.', 'success')
                else:
                    flash('Employee not found.', 'danger')
            else:
                flash('Missing employee id.', 'danger')
            return redirect(url_for('index'))

        # Update employee
        if action == 'update':
            emp_id = request.form.get('id')
            employee_id = request.form.get('employee_id')
            name = request.form.get('name')
            phone = request.form.get('phone')
            hourly_rate = request.form.get('hourly_rate')
            if emp_id and employee_id and name and phone and hourly_rate:
                db = get_db()
                db.execute('''
                    UPDATE employees
                    SET employee_id=?, name=?, phone=?, hourly_rate=?
                    WHERE id=?
                ''', (employee_id, name, phone, hourly_rate, emp_id))
                db.commit()
                db.close()
                flash('Employee updated.', 'success')
            else:
                flash('Missing fields for update.', 'danger')
            return redirect(url_for('index'))

        # Add new employee
        employee_id = request.form.get('employee_id')
        name = request.form.get('name')
        phone = request.form.get('phone')
        hourly_rate = request.form.get('hourly_rate')
        if employee_id and name and phone and hourly_rate:
            db = get_db()
            db.execute('''
                INSERT INTO employees (employee_id, name, phone, hourly_rate)
                VALUES (?, ?, ?, ?)
            ''', (employee_id, name, phone, hourly_rate))
            db.commit()
            db.close()
            flash('Employee added successfully.', 'success')
        else:
            flash('Missing fields for new employee.', 'danger')
        return redirect(url_for('index'))

    # GET: pagination
    try:
        page = max(int(request.args.get('page', 1)), 1)
    except ValueError:
        page = 1
    try:
        per_page = max(int(request.args.get('per', PER_PAGE_DEFAULT)), 1)
    except ValueError:
        per_page = PER_PAGE_DEFAULT
    offset = (page - 1) * per_page

    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM employees').fetchone()[0]
    employees = db.execute('SELECT * FROM employees ORDER BY id DESC LIMIT ? OFFSET ?', (per_page, offset)).fetchall()

    # Add total_hours from time_logs
    employees_with_hours = []
    for emp in employees:
        total_hours = db.execute(
            'SELECT SUM(hours_worked) FROM time_logs WHERE employee_id=?',
            (emp['employee_id'],)
        ).fetchone()[0] or 0
        emp_dict = dict(emp)
        emp_dict['total_hours'] = round(total_hours, 2)
        employees_with_hours.append(emp_dict)

    db.close()

    pages = max(1, math.ceil(total / per_page))
    has_prev = page > 1
    has_next = page < pages
    start_page = max(1, page - 2)
    end_page = min(pages, page + 2)

    return render_template(
        'index.html',
        employees=employees_with_hours,
        page=page, pages=pages, per_page=per_page,
        has_prev=has_prev, has_next=has_next, total=total,
        start_page=start_page, end_page=end_page
    )

# ----------------------------
# Clock in/out
# ----------------------------
@app.route('/clock', methods=['POST'])
def clock():
    employee_id = request.form.get('employee_id')
    action = request.form.get('action')  # clock_in or clock_out
    if not employee_id or not action:
        flash('Missing employee ID or action.', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    now = datetime.now()

    if action == 'clock_in':
        db.execute(
            'INSERT INTO time_logs (employee_id, clock_in) VALUES (?, ?)',
            (employee_id, now.isoformat(timespec='seconds'))
        )
        flash(f'Employee {employee_id} clocked in at {now.strftime("%H:%M:%S")}.', 'success')

    elif action == 'clock_out':
        log = db.execute(
            'SELECT * FROM time_logs WHERE employee_id=? AND clock_out IS NULL ORDER BY id DESC LIMIT 1',
            (employee_id,)
        ).fetchone()
        if log:
            clock_in_time = datetime.fromisoformat(log['clock_in'])
            delta_hours = (now - clock_in_time).total_seconds() / 3600
            db.execute(
                'UPDATE time_logs SET clock_out=?, hours_worked=? WHERE id=?',
                (now.isoformat(timespec='seconds'), delta_hours, log['id'])
            )
            flash(f'Employee {employee_id} clocked out at {now.strftime("%H:%M:%S")} ({delta_hours:.2f} hours).', 'success')
        else:
            flash('No clock-in found to clock out.', 'danger')

    db.commit()
    db.close()
    return redirect(url_for('index'))

# ----------------------------
# API for FullCalendar
# ----------------------------
@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    db = get_db()
    rows = db.execute('''
        SELECT s.id, s.date, s.start_time, s.end_time, e.name, s.employee_id
        FROM schedules s
        JOIN employees e ON s.employee_id = e.employee_id
    ''').fetchall()
    db.close()

    events = []
    for r in rows:
        events.append({
            "id": r['id'],
            "title": r['name'],
            "start": f"{r['date']}T{r['start_time']}",
            "end": f"{r['date']}T{r['end_time']}"
        })
    return jsonify(events)

@app.route('/api/schedules', methods=['POST'])
def add_schedule():
    data = request.json
    db = get_db()
    db.execute('''
        INSERT INTO schedules (employee_id, date, start_time, end_time)
        VALUES (?, ?, ?, ?)
    ''', (data['employee_id'], data['date'], data['start_time'], data['end_time']))
    db.commit()
    db.close()
    return jsonify({"status": "ok"})

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)

