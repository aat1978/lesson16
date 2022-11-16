from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils import init_database

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


if __name__ == "__main__":
    init_database()
    app.run(host="localhost", port=5000, debug=True)

