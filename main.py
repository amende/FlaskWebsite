import flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os



def create_app():
    # App and Database initialisation
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("secret_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    # Just for easier debug
    if os.getenv("debug"):
        db.drop_all()
        db.create_all()

    # Load environment variables
    load_dotenv()


    @app.route('/')
    def home():
        return flask.render_template('home.html')


    @app.route('/profile')
    def profile():
        return flask.render_template('notYet.html')


    @app.route('/signup')
    def signup():
        return flask.render_template('notYet.html')


    @app.route('/logout')
    def logout():
        return flask.render_template('notYet.html')


    @app.route('/login')
    def login():
        return flask.render_template('login.html')

    return(app)



# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
