import json
from flask import request
from app import app, db
from user import User


@app.route("/users", method=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for record in User.query.all():
            result.append(record.to_dict())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset==utl-8'}
    if request.method == "POST":
        user_data = json.loads(request.data)
        db.session.add(
            User(
                id=user_data.get("id"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                age=user_data.get("age"),
                email=user_data.get("email"),
                role=user_data.get("role"),
                phone=user_data.get("phone"),
            )
        )
        db.session.commit()
        return "", 201


@app.route("users/<int:vid>", methods=["GET", "PUT", "DELETE"])
def user(vid: int):
    if request.method == "GET":
        return json.dumps(User.query.get(vid).to_dist()), 200, {'Content-Type': 'application/json; charset==utl-8'}
    if request.method == "PUT":
        user_data = json.loads(request.data)
        new_user = User.query.get(vid)

        new_user.first_name = user_data["first_name"]
        new_user.last_name = user_data["last_name"]
        new_user.age = user_data["age"]
        new_user.email = user_data["email"]
        new_user.role = user_data["role"]
        new_user.phone = user_data["phone"]

        db.session.add(new_user)
        db.session.commit()
        return "", 201

    if request.method == "DELETE":
        delete_user = User.query.get(vid)
        db.session.add(delete_user)
        db.session.commit()
        return "", 204
