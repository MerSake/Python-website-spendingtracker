from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p>"

@auth.route('/logput')
def logout():
    return
@auth.route('/sgin-up')
def sign_up():
    return
