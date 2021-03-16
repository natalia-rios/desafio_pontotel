from flask import Flask, render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_user, login_required
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from . import db
from .models import User, OAuth

github_blueprint = make_github_blueprint(client_id = '444bb74d2138f007631c', client_secret = 'f1d0b31bff84a02079c4f1084ddd7bb98431eb2c')

google_blueprint = make_google_blueprint(client_id= "911164170871-eqppf9t37qndjt6mhnkj081gr3rj0ke2.apps.googleusercontent.com", client_secret= "21vQunK4GT1zmg2YRKDUq_xg",  scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
)
github_bp = make_github_blueprint(storage = SQLAlchemyStorage(OAuth, db.session, user = current_user))

google_bp = make_google_blueprint(storage = SQLAlchemyStorage(OAuth, db.session, user = current_user))

@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash("Não foi possível o login com Github.", category = "error")
        return
    resp = blueprint.session.get("/user")
    if not resp.ok:
        msg = "Falha ao coletar informações do usuário do Github."
        flash(msg, category= "error")
        return

    github_name = resp.json()["name"]
    github_user_id = resp.json()["id"]

    query = OAuth.query.filter_by(
        provider = blueprint.name, provider_user_id = github_user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        github_user_login = github_name
        oauth = OAuth(
            provider = blueprint.name,
            provider_user_id = github_user_id,
            provider_user_login = github_user_login,
            token = token,
        )

    if current_user.is_anonymous:
        if oauth.user:
            login_user(oauth.user)
            # flash("Successfully signed in with GitHub.", 'success')
        else:
            user = User(username = github_name)
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            # flash("Successfully signed in with GitHub.", 'success')
    else:
        if oauth.user:
            if current_user != oauth.user:
                url = url_for("auth.merge", username = oauth.user.username)
                return redirect(url)
        else:
            oauth.user =current_user
            db.session.add(oauth)
            db.session.commit()
            # flash("Successfully linked GitHub account.", 'success')

    return redirect(url_for("main.profile"))                        

@oauth_error.connect_via(github_blueprint)
def github_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response = {response}").format(
        name = blueprint.name, message = message, response = response
    )            
    flash(msg, category="error") 

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flask("Não foi possível fazer login com o Google.", category="error")
        return 
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Falha ao coletar informações do usuário do Google."
        flash(msg, category="error")
        return

    google_name = resp.json()["name"]
    google_user_id = resp.json()["id"]

    query = OAuth.query.filter_by(
        provider = blueprint.name, provider_user_id = google_user_id
    )    
    try:
        oauth = query.one()
    except NoResultFound:
        google_user_login = google_name

        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            provider_user_login=google_user_login,
            token=token,
        )
    if current_user.is_anonymous:        
        if oauth.user:
            login_user(oauth.user)
            # flash("Successfully signed in with Google.", 'success')
        else:
            user = User(username = google_name)

            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            # flash("Successfully signed in with Google.", 'success')
    else:
        if oauth.user:
            if current_user != oauth.user:
                url = url_for("auth.merge", username=oauth.user.username)
                return redirect(url)
        else:
            oauth.user = current_user
            db.session.add(oauth)
            db.commit()
            # flash("Successfully linked Google account.")

    return redirect(url_for("main.profile"))                        

@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message = message, response = response
    )    
    flash(msg, category = "error")
