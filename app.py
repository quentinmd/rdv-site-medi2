from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import qrcode
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

appointments = []

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'doctor': {'password': 'password123'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']

    appointment = {
        'name': name,
        'date': date,
        'time': time
    }
    appointments.append(appointment)

    qr_data = f'Nom: {name}\nDate: {date}\nHeure: {time}'
    qr_img = qrcode.make(qr_data)
    qr_img.save(os.path.join('static', 'qrcode.png'))

    return render_template('confirmation.html', name=name, date=date, time=time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('doctor'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect')

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/doctor')
@login_required
def doctor():
    return render_template('doctor.html', appointments=appointments)

@app.route('/api/appointments')
@login_required
def api_appointments():
    return jsonify(appointments)

if __name__ == '__main__':
    app.run(debug=True)
