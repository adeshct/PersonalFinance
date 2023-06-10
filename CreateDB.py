from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask

#Configuring the Flask App and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'  # SQLite database file
db = SQLAlchemy(app)

#Table for Categories
class Categories(db.Model):
    id = db.Column(db.Integer, nullable = True)
    cat_name = db.Column(db.String, primary_key = True)

    # __repr__ for debugging purposes
    def __repr__(self):
        return f"<Transaction {self.id}>"


#Table for transactions
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tran_date = db.Column(db.DateTime, nullable = False)
    payee = db.Column(db.String, nullable = False)
    description = db.Column(db.String(100), nullable=True)
    debit_amount = db.Column(db.Float, nullable=False)
    credit_amount = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(50), db.ForeignKey(Categories.cat_name), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # __repr__ for debugging purposes
    def __repr__(self):
        return f"<Transaction {self.id}>"

#Table for Budget
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    budget_category = db.Column(db.String, db.ForeignKey(Categories.cat_name), nullable = False)
    budget_amount = db.Column(db.Float, nullable = False)
    budget_spent = db.Column(db.Float, nullable = False)
    budget_remain = db.Column(db.Float, nullable = False)

    # __repr__ for debugging purposes
    def __repr__(self):
        return f"<Transaction {self.id}>"

#Table for Accounts
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    acc_name = db.Column(db.String, nullable = False)
    acc_type = db.Column(db.String, nullable = False)
    acc_bal = db.Column(db.Float, nullable = False)
    acc_init_bal = db.Column(db.Float, nullable = False)

    # __repr__ for debugging purposes
    def __repr__(self):
        return f"<Transaction {self.id}>"

#Table for Users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False) #Need to pass through encryption and store
    email_id = db.Column(db.String, nullable = False, unique = True)


    # __repr__ for debugging purposes
    def __repr__(self):
        return f"<Transaction {self.id}>"


with app.app_context():
    db.create_all()

with app.app_context():
    table = User.__table__
    print(table)