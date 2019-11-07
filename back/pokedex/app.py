from flask import Flask
from flask_cors import CORS
from flask_ngrok import run_with_ngrok

from werkzeug.middleware.proxy_fix import ProxyFix
from pokedex.api import register_api


def create_app():
    app = Flask(__name__)

    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    register_api(app)

    return app
