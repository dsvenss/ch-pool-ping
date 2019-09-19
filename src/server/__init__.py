from flask import Flask, escape, request
from .controller.main import main

app = Flask(__name__)

urlPrefix = "/"

app.register_blueprint(main, urlPrefix=urlPrefix)
