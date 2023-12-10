from flask import Flask,request,session,render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

from models import User

@app.route('/', methods=['GET','POST'])
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
            session['user_id'] = user.id        #storing user_id in session for later use
            return redirect('/dashboard')
        else:
            return render_template('login.html' , error="Invalid User")

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('dashboard.html', user  =  user )
      
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)

