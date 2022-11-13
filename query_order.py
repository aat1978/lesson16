import json
from flask import request
from app import app, db
from order import Order


@app.route("/orders", method=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for record in Order.query.all():
            result.append(record.to_dict())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset==utl-8'}
    if request.method == "POST":
        order_data = json.loads(request.data)
        db.session.add(
            Order(
                id=order_data.get("id"),
                name=order_data.get("name"),
                description=order_data.get("description"),
                start_date=order_data.get("start_date"),
                end_date=order_data.get("end_date"),
                address=order_data.get("address"),
                prise=order_data.get("prise"),
                customer_id=order_data.get("customer_id"),
                executor_id=order_data.get("executor_id"),
            )
        )
        db.session.commit()
        return "", 201


@app.route("orders/<int:vid>", methods=["GET", "PUT", "DELETE"])
def order(vid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(vid).to_dist()), 200, {'Content-Type': 'application/json; charset==utl-8'}
    if request.method == "PUT":
        order_data = json.loads(request.data)
        new_data = Order.query.get(vid)

        new_data.name = order_data["name"]
        new_data.description = order_data["description"]
        new_data.start_date = order_data["start_date"]
        new_data.end_date = order_data["end_date"]
        new_data.address = order_data["address"]
        new_data.prise = order_data["prise"]
        new_data.customer_id = order_data["customer_id"]
        new_data.executor_id = order_data["executor_id"]

        db.session.add(new_data)
        db.session.commit()
        return "", 201

    if request.method == "DELETE":
        delete_order = Order.query.get(vid)
        db.session.add(delete_order)
        db.session.commit()
        return "", 204
