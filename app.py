from flask import Flask, jsonify
from models import db
from auth.routes import auth_bp, bcrypt
from notes.routes import notes_bp
from flasgger import Swagger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///study.db"
app.config["SWAGGER"] = {
    "title": "AI Study Assistant API",
    "description": "An AI-powered API that generates summaries, quizzes, and study guides from user notes",
    "version": "1.0.0"
}

db.init_app(app)
bcrypt.init_app(app)

swagger = Swagger(app)

app.register_blueprint(auth_bp)
app.register_blueprint(notes_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Study Assistant API is running"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
