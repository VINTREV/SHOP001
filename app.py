from flask import Flask, render_template, request, redirect, url_for, session,flash
from werkzeug.security import check_password_hash, check_password_hash, generate_password_hash
from functools import wraps
import psycopg2
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret-key-123'
conn = psycopg2.connect(
    host="dpg-d1jka6u3jp1c73ecbfo0-a.oregon-postgres.render.com",
    database="postgresql_vintrev",
    user="postgresql_vintrev_user",
    password="DH200Hh5o7jeQgUCqLoTcE9s8inwKOhv",
    port="5432"
)
cursor= conn.cursor()

# Insert user
email = "vintrevlimited@gmail.com"
hashed_password = generate_password_hash("Vintrev@2025")

query = """
    INSERT INTO users (email, password_hash)
    VALUES (%s, %s)
"""
cursor.execute(query, (email, hashed_password))
conn.commit()

cursor.close()
conn.close()

# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        try:
            # IMPORTANT: create new connection for each request if outside app context
            conn = psycopg2.connect(
                host="dpg-d1jka6u3jp1c73ecbfo0-a.oregon-postgres.render.com",
                database="postgresql_vintrev",
                user="postgresql_vintrev_user",
                password="DH200Hh5o7jeQgUCqLoTcE9s8inwKOhv",
                port="5432"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                stored_hash = user[6]   # adjust index to match password_hash column position
                if check_password_hash(stored_hash, password):
                    session['user_id'] = user[0]
                    session['email'] = user[5]  # adjust index to match email column position
                    flash("Login successful", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Invalid email or password", "danger")
            else:
                flash("Invalid email or password", "danger")

        except Exception as e:
            conn.rollback()
            flash("Login error: " + str(e), "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template('logins.html', datetime=datetime)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('logins.html'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session.get('username'))

# Add similar routes for all your pages
@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html',  user=session.get('username'))

@app.route('/record_sale')
@login_required
def record_sale():
    return render_template('record_sale.html',  user=session.get('username'))

@app.route('/manage_users')
@login_required
def manage_users():
    return render_template('manage_users.html', user=session.get('username'))

@app.route('/roles_management')
@login_required
def roles_management():
    return render_template('roles_management.html',  user=session.get('username'))

@app.route('/permissions')
@login_required
def permissions():
    return render_template('permissions.html', user=session.get('username'))

@app.route('/onboarding')
@login_required
def onboarding():
    return render_template('onboarding.html',  user=session.get('username'))

@app.route('/sales_report')
@login_required
def sales_report():
    return render_template('sales_report.html',  user=session.get('username')) 

@app.route('/generate_report')
@login_required
def generate_report():
    return render_template('generate_report.html', user=session.get('username'))

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html',  user=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)
