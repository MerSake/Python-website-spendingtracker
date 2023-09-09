from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("/login.html", text="testing")

@auth.route('/logput')
def logout():
    return 0
@auth.route('/sgin-up')
def sign_up():
    return render_template("/sing-up.html")
