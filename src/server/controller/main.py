from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/start')
def start():
    return "Start"
