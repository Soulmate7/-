from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'guzehao20000912'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:guzehao20000912@127.0.0.1:3306/european'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    flag=0;
    db.init_app(app)


    from .face import face as face_blueprint
    app.register_blueprint(face_blueprint)
#
    return app
