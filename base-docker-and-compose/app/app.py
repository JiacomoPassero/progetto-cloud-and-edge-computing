from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from mixins import Serializer
import os
import json

app = Flask(__name__)
app.config["DEBUG"] = os.getenv('DEBUG', True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite://")
app.config["STATIC_FOLDER"] = f"{os.getenv('APP_FOLDER')}/static"
app.config["MEDIA_FOLDER"] = f"{os.getenv('APP_FOLDER')}/media"

db = SQLAlchemy(app)


class Worker(db.Model, Serializer):
    __tablename__ = "worker"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, fullname, email, active=active.default):
        self.fullname = fullname
        self.email = email
        self.active = bool(active)
    


# route to return all workers
@app.route('/api/v1/workers', methods=['GET'])
def index():
    workers = Worker.query.all()
    return json.dumps(Worker.serialize_list(workers))

# app.run()