# coding=utf-8


from flask import Blueprint, render_template, request, session

from modules.others.DatabaseUTILS import cur_execute
from modules.others.Settings import prefix, path_root
from modules.security import InputValidation

sign_up_api = Blueprint('sign_up_api', __name__)


@sign_up_api.route(prefix + 'signUp', methods=['POST'])
def sign_up_post():
    login = request.form['login']
    password = request.form['password']
    if not (InputValidation.verify_login(login) and InputValidation.verify_password(password)):
        return "Błędny input"
    res = cur_execute("SELECT login FROM users WHERE login = (?)", (login,))
    if len(res) > 0:
        return "Wybrany login już istnieje :-("
    cur_execute("INSERT INTO users VALUES(?, ?)", (login, password,))
    cur_execute("CREATE TABLE " + login + " ( note charset(255) )")
    session["login"] = login
    return render_template("menu.html", user=str(session["login"]), path_root=path_root)


@sign_up_api.route(prefix + 'signUp', methods=['GET'])
def sign_up_get():
    return render_template("signUp.html", path_root=path_root)