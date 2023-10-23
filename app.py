from flask import Flask,request,session,render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

from models import User

@app.route("/")
def index():
    return 'hi'

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(name = name, email = email , password = password)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template("register.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email = email).first()

        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/dashboard')
        else:
            return render_template('login.html' , error="Invalid User")

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if session['name']:
        user = User.query.all()
        return render_template('dashboard.html', user  =  user )
      
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)

