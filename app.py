from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  description TEXT,
                  amount REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    conn.close()

    # Group expenses by month and calculate totals
    monthly_totals = defaultdict(float)
    for expense in expenses:
        date = datetime.strptime(expense[1], '%Y-%m-%d')
        month_key = date.strftime('%Y-%m')
        monthly_totals[month_key] += expense[3]

    # Convert defaultdict to regular dict for template rendering
    monthly_totals = dict(monthly_totals)

    return render_template('index.html', expenses=expenses, monthly_totals=monthly_totals)

@app.route('/add', methods=['POST'])
def add_expense():
    date = request.form['date']
    description = request.form['description']
    amount = float(request.form['amount'])
    
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)",
              (date, description, amount))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
