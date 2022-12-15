from flask_app import app
from flask import render_template,redirect,request,session,flash
import flask_app
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/create_user', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    data = {
        "id": session['user_id'],
    }
    return render_template('login.html', users=User.single_user(data))

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/logging_in', methods=["POST"])
def logged_in():
    data = {
        "email": request.form['email']
    }
    user = User.get_user_by_email(data)
    if not user:
        flash("Incorrect Email.","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

    # the next thing we want to do is be able to log into with existing users, set up method to get email of user to verify when logging in. 
    # user = User.get_user_email(request.form), then right if loop to verify, if not user then redirect
    # make sure to session user_id when logging in. 