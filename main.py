from flask import Flask
from markupsafe import escape
from flask import render_template

from flask_restful import Api,Resource


app = Flask(__name__)

api= Api(app)
#import du module open id
from flask_oidc import OpenIDConnect

class myResource(Resource):
    def get(self):
        return({"key":"value"})

api.add_resource(myResource,"/api")
@app.route('/')
def index():
    return("hello, url dispos: login, api")
"""
@app.route('/')
def index():
    if oidc.user_loggedin:
        return 'Welcome %s' % oidc.user_getfield('email')
    else:
        return 'Not logged in'

@app.route('/login')
@oidc.require_login
def login():
    return 'Welcome %s' % oidc.user_getfield('email')



"""
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def do_the_login():
    if request.form['username']=="gabriel":
        return("bienvenue")
    else:
        return("non")

def show_the_login_form():
    return(render_template("form.html"))


if __name__=="__main__":
    app.run(debug=True)