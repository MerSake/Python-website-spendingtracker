from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['Get', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("/login.html", authorized=True)


@auth.route('/sign_up', methods=['Get', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 4:
            flash('Email must be greater the 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('Name must be longer then 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be longer then 6 characters', category='error')
        else:
            flash('Account created', category='success')
    return render_template("/sign_up.html")


@auth.route('/logout')
def logout():
    return 0


@auth.route('/home')
def Home():
    return render_template("/home.html")
