from flask import Blueprint, render_template 
from flask_login import login_required, current_user
from . import db 
from app import create_app
from flask import Flask

app = create_app()

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', username = current_user.username, email = current_user.email, password = current_user.password, country = current_user.country, state = current_user.state, city = current_user.city, CEP = current_user.CEP, rua = current_user.rua, numero = current_user.numero, complemento = current_user.complemento, CPF = current_user.CPF, PIS = current_user.PIS)

if __name__ == "__main__":
  app.run()