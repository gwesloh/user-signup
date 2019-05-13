from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user-signup:launchcode@localhost:8889/user-signup'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    def __init__(self, username, email, password):
        self.email = email
        self.password = password
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.email


@app.route("/")

def index():

    return render_template('index.html')


@app.route("/signup", methods= ['POST'])
def signup():
        username= request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if not char_present(username):
            flash('oh no! Username field is blank', category= 'username_error')
            return render_template('index.html')
        elif not char_present(password):
            flash('oh no! Password field is blank', category= 'password_error')
            return render_template('index.html')
        elif not char_present(verify):
            flash('oh no! Verify field is blank', category= 'verify_error')
            return render_template('index.html')
        elif not is_email(email):
            flash('oh no! "' + email + '" does not seem like an email address', category = 'email_error')
            return render_template('index.html')
        elif not is_username_or_pass(username):
            flash('oh no! "' + username + '" does not seem like a username', category= 'username_error')
            return render_template('index.html')
        elif not is_username_or_pass(password):
            flash('oh no! "' + password + '" does not seem like a password', category= 'password_error')
            return render_template('index.html')
        elif password != verify:
            flash('passwords did not match', category= 'verify_error')
            return render_template('index.html')
        else:
            
            user = User(email=email, password=password, username=username )
            session['user'] = user.username
            db.session.add(user)
            db.session.commit()
            User.query.filter_by(username=username)
        return render_template('welcome.html', title= 'Welcome Page', username= username)


def is_email(string):
   
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    char_not_present = len(string) == 0 
    email_present = len(string) >= 3
    space_index = string.find(' ')
    space_present = space_index >=0
    if not char_not_present and not email_present:
        return False
    elif not atsign_present:
        return False
    elif space_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

def is_username_or_pass(string):
   
    
    len_test_low = len(string) >= 3
    len_test_high = len(string) <= 20
    space_index = string.find(' ')
    space_present = space_index >=0
    if not len_test_low:
        return False
    elif not len_test_high:
        return False
    elif space_present:
        return False
    else:
        return True

def char_present(string):
    char_is_present = len(string) != 0
    if not char_is_present:
        return False
    else:
        return True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == "__main__":
    app.run()
