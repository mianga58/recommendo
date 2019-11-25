#importing the necessary libraries
from flask import Flask, render_template, flash, redirect, request, url_for, session, logging, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = 'secret123'

#Config MySQL
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
app.config['MYSQL_DATABASE_USER'] = 'b3eee2d3601c43'
app.config['MYSQL_DATABASE_PASSWORD'] = '9f8d73f5'
app.config['MYSQL_DATABASE_DB'] = 'heroku_c241604c99e7e47'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/predictor", methods=['GET','POST'])
def predictor():
  
    return render_template("predictor.html")

@app.route("/about")
def about():
    return render_template("about.html")

# REgister form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #create cursor
        cur = mysql.get_db().cursor()

        #Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #commit to DB
        mysql.get_db().commit()

        #close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        redirect(url_for('index'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
           if request.method == 'POST':
            # Get Form Fields
            username = request.form['username']
            password_candidate = request.form['password']

            #Create cursor
            cur = mysql.get_db().cursor()

            #Get user by username
            result = cur.execute("SELECT * FROM users WHERE username = %s",
                                 [username])

            if result > 0:
                # Get stored hash
                data = cur.fetchone()
                password = data['password']

                #Compare Password
                if sha256_crypt.verify(password_candidate, password):
                    #passed
                    session['logged_in'] = True
                    session['username'] = username

                    flash('You are now logged in', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid login'
                    return render_template("login.html", error=error)


            else:
               error = 'Username not found'
               return render_template("login.html", error=error)

           return render_template('login.html')
           # close connection
           cur.close()

#check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Twakwikata, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
