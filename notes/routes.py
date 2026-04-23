from flask import Blueprint, jsonify, request
from models import db, Note, User
from middleware import get_logged_in_user
import datetime
import requests as http_requests

notes_bp = Blueprint("notes", __name__)

from config import CLAUDE_API_KEY

def call_claude(prompt):
    response = http_requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    return data["content"][0]["text"]

def check_usage(user_id):
    user = User.query.get(user_id)
    if user.usage_count >= user.usage_limit:
        return False
    return True

def increment_usage(user_id):
    user = User.query.get(user_id)
    user.usage_count += 1
    db.session.commit()

@notes_bp.route("/notes", methods=["POST"])
def create_note():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "title" not in data or "content" not in data:
        return jsonify({"error": "title and content are required"}), 400
    note = Note(
        user_id=user["user_id"],
        title=data["title"],
        content=data["content"],
        created_at=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({"id": note.id, "title": note.title, "message": "Note created"}), 201

@notes_bp.route("/notes", methods=["GET"])
def get_notes():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    notes = Note.query.filter_by(user_id=user["user_id"]).all()
    result = []
    for n in notes:
        result.append({
            "id": n.id,
            "title": n.title,
            "has_summary": n.summary is not None,
            "has_quiz": n.quiz is not None,
            "has_study_guide": n.study_guide is not None,
            "created_at": n.created_at
        })
    return jsonify(result)

@notes_bp.route("/notes/<int:note_id>/summary", methods=["POST"])
def generate_summary(note_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    if not check_usage(user["user_id"]):
        return jsonify({"error": "Usage limit reached"}), 429
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    if note.user_id != user["user_id"]:
        return jsonify({"error": "This is not your note"}), 403
    try:
        summary = call_claude(f"Summarize these study notes in clear, concise bullet points:\n\n{note.content}")
        note.summary = summary
        increment_usage(user["user_id"])
        db.session.commit()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": "AI request failed", "details": str(e)}), 500

@notes_bp.route("/notes/<int:note_id>/quiz", methods=["POST"])
def generate_quiz(note_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    if not check_usage(user["user_id"]):
        return jsonify({"error": "Usage limit reached"}), 429
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    if note.user_id != user["user_id"]:
        return jsonify({"error": "This is not your note"}), 403
    try:
        quiz = call_claude(f"Generate 5 multiple choice quiz questions based on these notes. Include the correct answer for each:\n\n{note.content}")
        note.quiz = quiz
        increment_usage(user["user_id"])
        db.session.commit()
        return jsonify({"quiz": quiz})
    except Exception as e:
        return jsonify({"error": "AI request failed", "details": str(e)}), 500

@notes_bp.route("/notes/<int:note_id>/study-guide", methods=["POST"])
def generate_study_guide(note_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    if not check_usage(user["user_id"]):
        return jsonify({"error": "Usage limit reached"}), 429
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    if note.user_id != user["user_id"]:
        return jsonify({"error": "This is not your note"}), 403
    try:
        guide = call_claude(f"Create a comprehensive study guide from these notes. Include key concepts, definitions, and important points to remember:\n\n{note.content}")
        note.study_guide = guide
        increment_usage(user["user_id"])
        db.session.commit()
        return jsonify({"study_guide": guide})
    except Exception as e:
        return jsonify({"error": "AI request failed", "details": str(e)}), 500

@notes_bp.route("/usage", methods=["GET"])
def get_usage():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    db_user = User.query.get(user["user_id"])
    return jsonify({
        "usage_count": db_user.usage_count,
        "usage_limit": db_user.usage_limit,
        "remaining": db_user.usage_limit - db_user.usage_count
    })
