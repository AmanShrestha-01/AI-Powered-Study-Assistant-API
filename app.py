from flask import Flask, jsonify
from models import db
from auth.routes import auth_bp, bcrypt
from notes.routes import notes_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///study.db"

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(notes_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Study Assistant API is running"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
