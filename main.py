#importing the necessary libraries
from flask import Flask, render_template, flash, redirect, request, url_for, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import pandas as pd
import numpy as np
from flaskext.mysql import MySQL


# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# define a function that creates similarity matrix
# if it doesn't exist
def create_sim():
    data = pd.read_csv('data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return (data, sim)


# defining a function that recommends 10 most similar movies
def rcmd(m):
    m = m.lower()
    # check if data and sim are already assigned
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    # check if the movie is in our database or not
    if m not in data['course'].unique():
        return('This course is not in our database.\nPlease check if you spelled it correct.')
    else:
        # getting the index of the movie in the dataframe
        i = data.loc[data['course']==m].index[0]

        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

        # taking top 1- movie scores
        # not taking the first index since it is the same movie
        lst = lst[1:4]

        # making an empty list that will containg all 10 movie recommendations
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['course'][a])
        return l


app = Flask(__name__)


@app.route('/predictor')
def predictor():
    course = request.args.get('course')
    r = rcmd(course)
    course = course.upper()
    if type(r) == type('string'):
        return render_template('predictor.html', course=course, r=r, t='s')
    else:
        return render_template('predictor.html', course=course, r=r, t='l')

    mysql = MySQL()
    mysql.init_app(app)

#Config MySQL
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_PASSWORD'] = '9f8d73f5'
app.config['MYSQL_DATABASE_USER']= 'b3eee2d3601c43'
app.config['MYSQL_DATABASE_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DATABASE_DB']= 'users'
           


@app.route('/')
def index():
    return render_template("home.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")



@app.route('/predictor1',methods=['GET','POST'])
def predictor1():
    return render_template("predictor1.html")


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
            
            mysql.get_db().commit()

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
    app.secret_key = 'secret123'
    app.run(debug=True)
