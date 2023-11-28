from flask import Flask

app = Flask(__name__)

from app.route import uplord, view, search
