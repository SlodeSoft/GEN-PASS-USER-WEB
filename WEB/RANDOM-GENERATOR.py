import RandomPassword as Rdm
import os.path
import re
from lib import WEBTOMYSQL as CONNEC
from lib import SECRET as SCRT
from flask import Flask, render_template, request, session, redirect, url_for

__STATIC_DIR = os.path.abspath('./static')
__TEMPLATE_DIR = os.path.abspath('./templates')

app = Flask(__name__, static_folder=__STATIC_DIR, template_folder=__TEMPLATE_DIR)
title = "GEN TON PASS"
app.secret_key = 'O!c9]UE]b1j.,Fg]}^tJS/;5*)wTA=1BY{!}b#*002IJ+f)[E*'


class CONNECTION:
    def __init__(self):
        bddconn = CONNEC.CONNECT_TO_BDD()
        self.cursor = bddconn.connection.cursor()


bddcon = CONNECTION()
set_key = SCRT.__quatre__.__entry__.password
set_iv = SCRT.__cinq__.__entry__.password


class GENERATOR:
    def __init__(self, leng, numb, spechar, lowcase, uppcase):
        __step1__ = Rdm.RandomPassword()
        self.__passwd__ = __step1__.generate_random_password(length=leng,
                                                             include_numbers=numb,
                                                             include_special_characters=spechar,
                                                             include_lower_case_alphabets=lowcase,
                                                             include_upper_case_alphabets=uppcase)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',
                               stylelogin="./static/stylelogin.css",
                               title=title)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL

        sql = 'CALL `SELECT_CRYPT_USER_INFO`(%s, %s, %s, %s)'
        values = (set_key,
                  set_iv,
                  username,
                  password)
        bddcon.cursor.execute(sql, values)
        # Fetch one record and return result
        account = bddcon.cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to Home Page
            return redirect(url_for('generatorweb'))
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html',
                           stylelogin="./static/stylelogin.css",
                           title=title, msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form \
            and 'password' in request.form \
            and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        sql = "CALL `SELECT_REGISTRY_USER`(%s, %s, %s)"
        values = (set_key,
                  set_iv,
                  username)
        bddcon.cursor.execute(sql, values)
        account = bddcon.cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            print(account[0])
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            sql = "CALL `INSERT_CRYPT_USER_INFO`(%s, %s, %s, %s, %s)"
            values = (set_key,
                      set_iv,
                      username,
                      password,
                      email)
            bddcon.cursor.execute(sql, values)
            bddcon.cursor.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html',
                           stylelogin="./static/stylelogin.css",
                           msg=msg)


@app.route('/gen', methods=['GET', 'POST'])
def generatorweb():
    if 'loggedin' in session:
        labellist = ("Include Number",
                     "Include Special Characters",
                     "Include Lower Case",
                     "Include UPPER Case")
        namelist = ("selector-2",
                    "selector-3",
                    "selector-4",
                    "selector-5")
        if request.method == "POST":
            form = request.form
            allarglist = list()
            leng = request.form.get('selector-1')
            num = request.form.get('selector-2')
            spechar = request.form.get('selector-3')
            lowcas = request.form.get('selector-4')
            uppcas = request.form.get('selector-5')
            allarglist.extend([num, spechar, lowcas, uppcas])
            gen = GENERATOR(int(leng), num, spechar, lowcas, uppcas)
            tachaine = gen.__passwd__
            return render_template('index.html', extract=tachaine,
                                   stylesgeneral="./static/stylesgeneral.css",
                                   stylesselection="./static/stylesselection.css",
                                   title=title,
                                   leng=leng,
                                   labellist=labellist,
                                   zip=zip,
                                   namelist=namelist,
                                   allarglist=allarglist,
                                   form=form)
        if request.method == "GET":
            leng = 20
            gen = GENERATOR(20, True, True, True, True)
            tachaine = gen.__passwd__
            return render_template("index.html", extract=tachaine,
                                   stylesgeneral="./static/stylesgeneral.css",
                                   stylesselection="./static/stylesselection.css",
                                   title=title,
                                   labellist=labellist,
                                   namelist=namelist,
                                   leng=leng,
                                   zip=zip)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                           stylesgeneral="./static/stylesgeneral.css",
                           styles404="./static/styles404.css",
                           favicon='./static/img/favicon.png',
                           title=title), 404


if __name__ == "__main__":
    app.run(debug=True, port=80)
