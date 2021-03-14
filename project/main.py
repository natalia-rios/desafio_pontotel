from flask import Blueprint, render_template 
from flask_login import login_required, current_user
from project import create_app, db
from flask import Flask
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', username = current_user.username, email = current_user.email, password = current_user.password, country = current_user.country, state = current_user.state, city = current_user.city, CEP = current_user.CEP, rua = current_user.rua, numero = current_user.numero, complemento = current_user.complemento, CPF = current_user.CPF, PIS = current_user.PIS)

if '__main__':
  app = create_app()
  try:
    with app.app_context():
      db.create_all()
  except OperationalError: 
    None
  HOST = os.environ.get("SERVER_HOST", "localhost")
  try:
    PORT = int(os.environ.get("SERVER_PORT", "5000"))
  except ValueError:
    PORT = 5001
  app.run(HOST, PORT, threaded=True)
