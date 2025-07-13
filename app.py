from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secret-key-123'

# Hardcoded users
valid_users = {
    'admin': '123456',
    'manager': 'managerpw',
    'agent': 'agentpw'
}
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
        username = request.form.get('username')
        password = request.form.get('password')

        if username in valid_users and valid_users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password!"
            return render_template('logins.html', error=error)
    return render_template('logins.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session.get('username'))

# Add similar routes for all your pages
@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html',  user=session.get('username'))

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

@app.route('/record_sale')
@login_required
def record_sale():
    return render_template('record_sale.html',  user=session.get('username'))

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
