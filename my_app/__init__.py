import os
from flask import Flask, request,redirect,make_response,url_for
from my_app.controllers.database import init_db
from my_app.controllers.auth import authBp
from my_app.controllers.users import usersBp
from my_app.controllers.movies import moviesBp



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return make_response(redirect(url_for('auth.login')))
     
    with app.app_context():
        init_db()
    
    app.register_blueprint(authBp)
    app.register_blueprint(moviesBp)

    return app