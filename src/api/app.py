from flask import Flask

from controllers.genericos_bp import generico_bp

DEFAULT_HOST =  "0.0.0.0"

app = Flask(__name__)


def start_server(port: int):
    app.register_blueprint(generico_bp)
    app.run(host=DEFAULT_HOST,port=port)