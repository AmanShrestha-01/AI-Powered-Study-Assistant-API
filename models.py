from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    usage_count = db.Column(db.Integer, default=0)
    usage_limit = db.Column(db.Integer, default=50)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    quiz = db.Column(db.Text, nullable=True)
    study_guide = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.String, nullable=False)
