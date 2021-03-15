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

  user= User.query.filter_by(email=email).first()
  CPF_login = User.query.filter_by(CPF=email).first()
  PIS_login = User.query.filter_by(PIS=email).first()
  
  login_errors = False

  if (not user and not CPF_login and not PIS_login):
    flash('Seu email/PIS/CPF está incorreto. Digite as informações corretamente.', 'danger')
    login_errors = True
  if CPF_login:
    if not check_password_hash(CPF_login.password, password):
      flash('Sua senha está incorreta. Digite as informações corretamente.', 'danger')
      login_errors = True
  if user:
    if not check_password_hash(user.password, password):
      flash('Sua senha está incorreta. Digite as informações corretamente.', 'danger')
      login_errors = True
  if PIS_login:
    if not check_password_hash(PIS_login.password, password):
      flash('Sua senha está incorreta. Digite as informações corretamente.', 'danger')
      login_errors = True
  
  if login_errors:
    return redirect(url_for('auth.login'))

  if user and not login_errors:
    login_user(user, remember=remember)
  if CPF_login and not login_errors:
    login_user(CPF_login, remember=remember)
  if PIS_login and not login_errors:
    login_user(PIS_login, remember=remember)


  return redirect(url_for('main.profile')) 

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
  CEP = request.form.get('CEP')

  user = User.query.filter_by(email=email).first()
  CPF_flash = User.query.filter_by(CPF=CPF).first()
  PIS_flash = User.query.filter_by(PIS=PIS).first()

  errors = False

  if user:
    flash('Endereço de email já existe')
    errors = True
  
  if CPF_flash:
    flash('CPF já existe')
    errors = True

  if PIS_flash:
    flash('PIS já existe')
    errors = True

  if errors:
    return redirect(url_for('auth.signup'))
  
  new_user = User(username = username, email = email, password = generate_password_hash(password, method='sha256'), city = city, country = country, state = state, rua = rua, numero = numero, complemento = complemento, CPF = CPF, PIS = PIS, CEP = CEP)

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

  return redirect(url_for('main.profile'))