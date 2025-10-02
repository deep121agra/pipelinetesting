from flask import request, jsonify, abort
from .models import Todo
from . import db

def serialize(todo):
    return {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'is_done': todo.is_done,
        'created_at': todo.created_at.isoformat(),
    }

def init_app(app):
    @app.route('/todos', methods=['GET'])
    def list_todos():
        todos = Todo.query.all()
        return jsonify([serialize(t) for t in todos])

    @app.route('/todos', methods=['POST'])
    def create_todo():
        data = request.get_json() or {}
        if not data.get('title'):
            abort(400, "Title is required")
        todo = Todo(
            title=data['title'],
            description=data.get('description', "")
        )
        db.session.add(todo)
        db.session.commit()
        return jsonify(serialize(todo)), 201

    @app.route('/todos/<int:todo_id>', methods=['PATCH'])
    def update_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json() or {}
        if 'title' in data:
            todo.title = data['title']
        if 'description' in data:
            todo.description = data['description']
        if 'is_done' in data:
            todo.is_done = data['is_done']
        db.session.commit()
        return jsonify(serialize(todo))

    @app.route('/todos/<int:todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"})
