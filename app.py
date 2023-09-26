from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'FFFFDDDDSSSS'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://viktor:311991@db:3306/flask_app?charset=utf8mb4'
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


import routes.routes

if __name__ == '__main__':
    app.run(debug=True)
