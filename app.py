from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import util

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URT'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


if __name__ == "__mane__":
    util.init_database()
    app.run(debug=True)
