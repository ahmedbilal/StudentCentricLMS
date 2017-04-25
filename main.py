# core library
from flask import Flask, render_template, redirect, url_for, g, app, request

# library to connect postgresQL
import psycopg2

# libraries to create forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename



class JoinForm(FlaskForm):
    name = StringField("name", validators = [DataRequired()])
    roll = StringField("roll number", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
class LoginForm(FlaskForm):
    roll = StringField("roll number")
    password = PasswordField("password")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'



#def get_db():
#    db = getattr(g, '_database', None)
#    if db is None:
#        db = g._database = psycopg2.connect("dbname=ahmedbilalkhalid user=postgres")
#        return db

#@app.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()

@app.route('/')
def index():
    return render_template("index.html", title="Homepage", header=True)

@app.route('/login', methods = ('GET', 'POST'))
def login():
    conn = get_db()
    cur = conn.cursor()
    form = LoginForm()
    if request.method == "POST":
        roll = form.roll.data
        password = form.password.data
        cur.execute("SELECT COUNT(*) FROM \"Users\" WHERE roll=%s AND password=%s",(roll, password))
        result = cur.fetchone()
        print(result)
        if result[0] != 0:
            return "Logged in"
        else:
            return "roll number or password incorrect"
    return render_template("login.html", title="Login", form=form)

@app.route('/join', methods = ('GET', 'POST'))
def join():
    conn = get_db()
    cur = conn.cursor()
    form = JoinForm()
    if form.validate_on_submit():
        name = form.name.data
        roll = form.roll.data
        password = form.password.data
        cur.execute("INSERT INTO \"Users\" (name, roll, password) VALUES (%s, %s, %s)",(name, roll, password))
        conn.commit()
        return redirect(url_for('joinSuccess'))
    return render_template("join.html", title="Join", form = form)


@app.route('/joinSuccess')
def joinSuccess(user_key):
    return render_template("joinSuccess.html", title="Successfully Joined")

if __name__== '__main__':
    app.run()
