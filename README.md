# Employee Management System

A simple web-based employee management system built with **Flask** and **SQLite**.
This application allows you to manage employees, track their work hours, and calculate total hours worked.

---

## Features

* **Employee Management**

  * Add, edit, and delete employees
  * Fields: Employee ID, Name, Phone, Hourly Rate
* **Clock In / Clock Out**

  * Track employee working hours
  * Automatically calculates hours worked per shift
* **Total Hours**

  * Displays total hours worked per employee
* **Pagination**

  * Efficiently browse large employee lists
* **Flash Messages**

  * Feedback for all actions (add, edit, delete, clock in/out)

---

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> **Dependencies:**
>
> * Flask
> * SQLite (built-in Python module)

---

## Usage

1. **Initialize the database**

```bash
python app.py
```

The first run will create the necessary tables: `employees` and `time_logs`.

2. **Generate test data (optional)**

```bash
python test_data.py
```

This will create 10 test employees with random hourly rates.

3. **Run the application**

```bash
python app.py
```

Access the app in your browser at: `http://localhost:5000`

---

## File Structure

```
.
├── app.py              # Main Flask application
├── test_data.py        # Script to generate test employees
├── employees.db        # SQLite database (created automatically)
├── templates/
│   └── index.html      # HTML template
├── static/
│   ├── css/style.css   # Optional custom styles
│   └── js/app.js       # Optional JS for search/filtering
└── README.md           # Project documentation
```

---

## How to Use

### Adding an Employee

* Fill out **Employee ID**, **Name**, **Phone**, and **Hourly Rate** in the form and click **Add Employee**.

### Editing an Employee

* Click **Edit** next to the employee.
* Update fields in the modal and click **Save Changes**.

### Deleting an Employee

* Click **Delete** next to the employee.
* Confirm deletion in the popup.

### Clocking In/Out

* Use **Clock In** / **Clock Out** buttons next to each employee.
* Hours worked are automatically calculated and added to the total.

### Pagination & Search

* Use pagination at the bottom to navigate large employee lists.
* Filter/search employees using the search box.

---

## Notes

* The app stores data in a local **SQLite database** (`employees.db`).
* For production, it is recommended to use a stronger `SECRET_KEY` via environment variables.
* Hourly rates are decimal values; total hours are calculated to 2 decimal points.

---

## License

This project is open-source and available under the MIT License.
