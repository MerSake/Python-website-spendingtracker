from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import datetime
from sqlalchemy import extract
from . import db
from .models import Expenses
import pygal 
import calendar


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("/home.html", user=current_user)


@views.route('/monthlyExpenses', methods=['Get', 'POST'])
@login_required
def expenses():
    
    expenses = Expenses.query.filter(extract('month', Expenses.date) == datetime.date.today().month).all()
    
    
    total_expenses = {
    'groceriesEx': 0,
    'ordersEx': 0,
    'HomeEx': 0,
    'restaurantEx': 0,
    'otherExpensesEx': 0
    }
    
    for expense in expenses:
        total_expenses['groceriesEx'] += expense.groceriesEx
        total_expenses['ordersEx'] += expense.ordersEx
        total_expenses['HomeEx'] += expense.HomeEx
        total_expenses['restaurantEx'] += expense.restaurantEx
        total_expenses['otherExpensesEx'] += expense.otherExpensesEx
        
    total = total_expenses['groceriesEx']+total_expenses['ordersEx']+total_expenses['HomeEx']+total_expenses['restaurantEx']+total_expenses['otherExpensesEx'] 
    
    chart = pygal.Pie()
    chart.title = "Expenses of " + calendar.month_name[datetime.date.today().month]
    chart.add('Groceries expenses', total_expenses['groceriesEx'])
    chart.add('Orders expenses', total_expenses['ordersEx'])
    chart.add('Home expenses', total_expenses['HomeEx'])
    chart.add('Restaurant expenses', total_expenses['restaurantEx'])
    chart.add('Other expenses', total_expenses['otherExpensesEx'])
    
    
    if request.method == 'POST':
        groceries = request.form.get('groceries')
        orders = request.form.get('orders')
        Home = request.form.get('Home')
        restaurant = request.form.get('restaurant')
        otherExpenses = request.form.get('otherExpenses')
        notes = request.form.get('notes')
        if Expenses.query.filter_by(date=datetime.date.today()).first():
            user = Expenses.query.filter_by(date=datetime.date.today()).first()
            if groceries != '':
                user.groceriesEx += int(groceries)
            if orders != '':
                user.ordersEx += int(orders)
            if Home != '':
                user.HomeEx += int(Home)
            if restaurant != '':
                user.restaurantEx += int(restaurant)
            if otherExpenses != '':
                user.otherExpensesEx += int(otherExpenses)
            user.notes += "\n|" + notes
            db.session.commit()
        else:
            new_record = Expenses(date=datetime.date.today(), groceriesEx=groceries, ordersEx=orders, HomeEx=Home, restaurantEx=restaurant, otherExpensesEx=otherExpenses, notes=notes)
            db.session.add(new_record)
            db.session.commit()
        
        return redirect(url_for('views.expenses'))
    
    chart = chart.render_data_uri()
    return render_template("/monthlyExpenses.html", user=current_user, chart = chart)
