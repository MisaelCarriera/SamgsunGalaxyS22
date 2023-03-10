from crypt import methods
from unicodedata import name
from flask import Flask , redirect , render_template , request, url_for , session , flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false

app = Flask(__name__)
app.secret_key = "Hello"
app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id' , db.Integer , primary_key=True)
    name = db.Column('nm' , db.String(100))
    email = db.Column('email' , db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/second')
def second():
    return render_template('second.html')

@app.route("/login" , methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session['user'] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("login successful!")
        return redirect(url_for("user"))
    else:
        if 'user' in session:
            flash("Already logged in!")
            return redirect(url_for('user'))

    return render_template('login.html')

@app.route('/user' , methods=["POST", "GET"])
def user():
    email = None
    if"user" in session:
        user = session["user"]

        if request.method == "POST" :
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit
            flash('email was saved')
        else:
            if email in session:
                email = session["email"]

        return render_template("user.html", email = email)
    else:
        flash("you are now logged in!")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user' , None)
    flash("you have been logged out!" , "info")
    return redirect(url_for('login'))

@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
