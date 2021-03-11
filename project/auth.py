from flask import Blueprint, render_template, redirect, url_for, request, flash 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_jwt_extended import jwt_required, create_access_token
from .models import User, OAuth
from . import db, mail
import os
from sqlalchemy import or_

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
  return render_template('login.html') 

@auth.route('/login', methods=['POST']) 
def login_post():
  email = request.form.get('email')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  user = User.query.filter_by(email=email).first()
    
  if not user or not check_password_hash(user.password, password):
    flash('Seu email/PIS/CPF ou senha estão incorretos. Digite as informações corretamente.', 'danger')
    return redirect(url_for('auth.login'))

  login_user(user, remember=remember)

  return redirect(url_for('main.profile')) 

def send_email(user):
  token = user.get_reset_token()

  msg = Message()
  msg.subject = "Login System: Password Reset Request"
  msg.sender = 'username@gmail.com'
  msg.recipients = [user.email]
  msg.html = render_template('reset_pwd.html', user = user, token = token)

  mail.send(msg)

@auth.route('/reset', methods=['GET','POST'])
def reset():
  if request.method == "GET":
    return render_template('reset.html')

  if request.method == "POST":
    email = request.form.get('email')
    user = User.verify_email(email)

    if user:
      send_email(user)
      flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('auth.login')) 
  
@auth.route('/reset/<token>', methods = ['GET', 'POST'])
def reset_verified(token):
  user = User.verify_reset_token(token)

  if not user:
    flash('User not found or token has expired', 'warning')
    return redirect(url_for('auth.reset'))

  password = request.form.get('password')
  # if len(password or ()) < 8:
  #   flash('Your password needs to be at least 8 characters', 'error')     
  if password:
    hashed_password = generate_password_hash(password, method='sha256')
    user.password = hashed_password

    db.session.commit()
    flash('Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('auth.login'))
  return render_template('reset_password.html')    

@auth.route('/signup')
def signup():
  return render_template('signup.html')
  
@auth.route('/signup', methods=['POST'])
def signup_post():
  username = request.form.get('username')
  email = request.form.get('email')
  password = request.form.get('password')
  city = request.form.get('city')
  country = request.form.get('country')
  state = request.form.get('state')
  rua = request.form.get('rua')
  numero = request.form.get('numero')
  complemento = request.form.get('complemento')
  CPF = request.form.get('CPF')
  PIS = request.form.get('PIS')

  user = User.query.filter_by(email=email).first()
  CPF = User.query.filter_by(CPF=CPF).first()
  PIS = User.query.filter_by(PIS=PIS).first()

  errors = False

  if user:
    flash('Endereço de email já existe')
    errors = True
  
  if CPF:
    flash('CPF já existe')
    errors = True

  if PIS:
    flash('PIS já existe')
    errors = True

  if errors:
    return redirect(url_for('auth.signup'))
  
  new_user = User(username = username, email = email, password = generate_password_hash(password, method='sha256'), city = city, country = country, state = state, rua = rua, numero = numero, complemento = complemento, CPF = CPF, PIS = PIS)

  db.session.add(new_user)
  db.session.commit()

  return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))  

@auth.route('/update')
def update():
  return render_template('update_data.html')
  
@auth.route('/update', methods=['POST'])
def update_post():

  #user = User.query.filter_by(email = current_user.email).first() 

  new_username = request.form.get('username')
  new_email = request.form.get('email')
  new_password = request.form.get('password')
  new_city = request.form.get('city')
  new_country = request.form.get('country')
  new_state = request.form.get('state')
  new_rua = request.form.get('rua')
  new_numero = request.form.get('numero')
  new_complemento = request.form.get('complemento')
  new_cep = request.form.get('CEP')
  new_cpf = request.form.get('CPF')
  new_pis = request.form.get('PIS')

  check_user = User.query.filter_by(email=new_email).first()
  check_CPF = User.query.filter_by(CPF=new_cpf).first()
  check_PIS = User.query.filter_by(PIS=new_pis).first()

  errors = False

  if check_user:
    flash('Endereço de email já existe')
    errors = True
  
  if check_CPF:
    flash('CPF já existe')
    errors = True

  if check_PIS:
    flash('PIS já existe')
    errors = True

  if errors:
    return redirect(url_for('auth.update'))

  if new_username:
    current_user.username = new_username

  if new_email:
    current_user.email = new_email

  if new_password:
    current_user.password = new_password

  if new_city:
    current_user.city = new_city 

  if new_country:
    current_user.country = new_country

  if new_state:
    current_user.state = new_state

  if new_rua:
    current_user.rua = new_rua

  if new_numero:
    current_user.numero = new_numero

  if new_complemento:
    current_user.complemento = new_complemento

  if new_cep:
    current_user.CEP = new_cep

  if new_pis:
    current_user.PIS = new_pis

  if new_cpf:
    current_user.CPF = new_cpf

  db.session.commit()

  return redirect(url_for('auth.login'))

  