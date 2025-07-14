from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import psycopg2

app = Flask(__name__)
app.secret_key = 'secret-key-123'

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d1jka6u3jp1c73ecbfo0-a.oregon-postgres.render.com",
        database="postgresql_vintrev",
        user="postgresql_vintrev_user",
        password="DH200Hh5o7jeQgUCqLoTcE9s8inwKOhv",
        port="5432"
    )
    return conn

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please login first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Create users table if not exists
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()

    # Check if the default user exists
    cursor.execute("SELECT * FROM users WHERE email=%s", ("vintrevlimited@gmail.com",))
    user = cursor.fetchone()
    if not user:
        hashed_password = generate_password_hash("Vintrev@2025")
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            ("vintrevlimited@gmail.com", hashed_password)
        )
        conn.commit()

    cursor.close()
    conn.close()

# Routes

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            user_email = user[1]
            user_password_hash = user[2]
            if check_password_hash(user_password_hash, password):
                session['username'] = user_email
                flash("Login successful.", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid password.", "danger")
        else:
            flash("Email not found.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html')

@app.route('/manage_users')
@login_required
def manage_users():
    return render_template('manage_users.html')

@app.route('/roles_management')
@login_required
def roles_management():
    return render_template('roles_management.html')

@app.route('/permissions')
@login_required
def permissions():
    return render_template('permissions.html')

@app.route('/onboarding')
@login_required
def onboarding():
    return render_template('onboarding.html')

@app.route('/sales_report')
@login_required
def sales_report():
    return render_template('sales_report.html')

@app.route('/record_sale')
@login_required
def record_sale():
    return render_template('record_sale.html')

@app.route('/generate_report')
@login_required
def generate_report():
    return render_template('generate_report.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    create_users_table()
    app.run(debug=True)
