from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash

from CreateDB import *
from werkzeug.security import generate_password_hash, check_password_hash

# Configuring the Flask App and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'  # SQLite database file
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# Home Page
@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/transaction_list')
@login_required
def transaction_list():
    transactions = Transaction.query.all()
    return render_template('transaction.html', transactions=transactions)


# Add transaction
@app.route('/transacions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        description = request.form['description']
        tran_date = datetime(request.form['tran_date'])
        payee = request.form['payee']
        debit_amount = float(request.form['debit_amount'])
        credit_amount = float(request.form['credit_amount'])
        category = request.form['category']
        timestamp = datetime.utcnow()

        transaction = Transaction(description=description, tran_date=tran_date, payee=payee,
                                  debit_amount=debit_amount, credit_amount=credit_amount, category=category,
                                  timestamp=timestamp)
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('transaction_list'))
    categories = Categories.query.all()
    return render_template('add_transaction.html', categories=categories)


@app.route('/budgets/add', methods=['GET', 'POST'])
@login_required
def add_budget():
    if request.method == 'POST':
        budget_category = request.form['budget_category']
        budget_amount = float(request.form['budget_amount'])
        budget_spent = float(request.form['budget_spent'])
        budget_remain = float(request.form['budget_spent'])

        budgets = Budget(budget_category=budget_category, budget_amount=budget_amount, budget_spent=budget_spent,
                         budget_remain=budget_remain)

        db.session.add(budgets)
        db.session.commit()

        return redirect(url_for('budget_list'))
    budgets = Budget.query.all()
    return render_template('add_budget.html', budgets=budgets)


@app.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_categories():
    if request.method == 'POST':
        cat_name = request.form['cat_name']

        category = Categories(cat_name=cat_name)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('categories_list'))
    categories = Categories.query.all()
    return render_template('add_categories.html', categories=categories)


@app.route('/budget')
@login_required
def budget_list():
    budgets = Budget.query.all()
    return render_template('budget.html', budgets=budgets)


@app.route('/categories')
@login_required
def categories_list():
    categories = Categories.query.all()
    return render_template('categories.html', categories=categories)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email_id = request.form['email_id']
        password = request.form['password']
        confirm_password =request.form['confirm_password']

        if password!= confirm_password:
            flash("Passwords do not match!! Try Again!!",'error')
            return redirect(url_for('signup'))

        existing_user = 1#User.query.filter_by(email_id = email_id).first()
        if existing_user:
            flash("Email ID already exist. Kindly signup", 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(email_id = email_id, password = hashed_password, name = name)
        db.session.add(user)
        db.session.commit()

        flash('Signup successful. You can now log in', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #user_name = request.form['user_name']
        password = request.form['password']
        email_id = request.form['email_id']
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email_id = email_id).first()

        if user and user.password == password:
            login_user(user, remember = remember)
            return redirect(url_for(home))
        else:
            return render_template('login.html', error = 'Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.html'))


if __name__ == '__main__':
    app.run()
