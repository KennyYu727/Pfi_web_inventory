# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 11:46:08 2019

@author: kenny
"""
# import statement 
import sqlite3 as sql
import sys

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user,current_user,login_required
# -----------------------------------------------------------------------------
# ******************************************
# test test test
import variable_names as vbn
dash_name = vbn.dashboard_names()
dash_name.initialize_name()

# ******************************************

app = Flask(__name__)
app.config['SECRET_KEY']= 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -----------------------------------------------------------------------------
class Product(UserMixin,db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(15), unique=True)
    product_quantity = db.Column(db.String(15)) 
    product_store_location = db.Column(db.String(15))
    
    def __init__(self,product_name,product_quantity,product_store_location):
        self.product_name = product_name
        self.product_quantity = product_quantity
        self.product_store_location = product_store_location
    def __repr__(self):
        return '<Product %r>' % self.product_name
               
# Database class
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


# -----------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------------------------------------------------------
# Form class 
class LoginForm(FlaskForm):
    
    username = StringField('User name', validators=[InputRequired(),Length(min=4,max=15)])
    password= PasswordField('Password', validators=[InputRequired(),Length(min=8,max=80)])
    remember = BooleanField('Remember Me')
    
class RegisterForm(FlaskForm):
    
    username = StringField('User name', validators=[InputRequired(),Length(min=4,max=15)])
    email = StringField('Email', validators=[InputRequired(),Email(message='Invalid Email'), Length(max=80)])
    password= PasswordField('Password', validators=[InputRequired(),Length(min=8,max=80)])
    
class AddNewProductForm(FlaskForm):
    
    product_name = StringField('Product Name',validators=[InputRequired(),Length(min=4,max=15)])
    product_quantity = StringField('Product quantity',validators=[InputRequired(),Length(min=4,max=15)])
    product_store_location = StringField('Product location',validators=[InputRequired(),Length(min=4,max=15)])
  
class ModifyProductQuantityForm(FlaskForm):
    
    modify_value = StringField('Change The Quantity',validators=[InputRequired(),Length(min=1,max=15)])
       
# -----------------------------------------------------------------------------  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + " " + form.password.data + '</h1>'
        
    return render_template('login.html',form = form)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = RegisterForm() 
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user created</h1>'
        #return '<h1>' + form.username.data + " " + form.email.data + " " + form.password.data + '</h1>'
    return render_template('signup.html',form = form)

@app.route('/addproduct', methods = ['GET','POST'])
def addproduct():
    form = AddNewProductForm() 
    
    if form.validate_on_submit():

        new_product = Product(product_name = form.product_name.data,
                              product_quantity = form.product_quantity.data,
                              product_store_location = form.product_store_location.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('dashboard'))
        # return '<h1>New Product created</h1>'

        #return '<h1>' + form.username.data + " " + form.email.data + " " + form.password.data + '</h1>'
    return render_template('addproduct.html',form = form)


@app.route('/modifyproductquantity', methods = ['GET','POST'])
def modifyproductquantity():
    form = ModifyProductQuantityForm()
    my_product = Product.query.all()
    
    if form.validate_on_submit():

        selected_value = request.form['value']
        modified_target = Product.query.filter_by(product_name = selected_value).first()
        modified_target.product_quantity = form.modify_value.data

        con = sql.connect('database.db')
        execute_query = "UPDATE product SET product_quantity =" + form.modify_value.data  + " WHERE product_name =" + "'" +selected_value + "'" 
          
        with con:
            cur = con.cursor()    
            cur.execute(execute_query)
                
        #temp = form.modify_value.data
        return redirect(url_for('dashboard'))
        #return '<h1>' + temp + '</h1>'
    
    return render_template('modifyproductquantity.html',
                           form = form,
                           my_product = my_product)



# -----------------------------------------------------------------------------  
@app.route('/dashboard_')
@login_required
def dashboard_():
    return render_template('dashboard_test.html',name = current_user.username)

@app.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
    
    my_product = Product.query.all()
    
    return render_template('dashboard.html',
                           name = current_user.username,
                           test = dash_name.bread,
                           my_product = my_product)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
    
    
    
    