import json
from flask import request
from app import app, db
from offer import Offer


@app.route("/offers", method=["GET", "POST"])
def offers():
    if request.method == "GET":
        result = []
        for record in Offer.query.all():
            result.append(record.to_dict())
        return json.dumps(result), 200, {'Content-Type': 'application/json; charset==utl-8'}
    if request.method == "POST":
        offer_data = json.loads(request.data)
        db.session.add(
            Offer(
                id=offer_data.get("id"),
                order_id=offer_data.get("order_id"),
                executor_id=offer_data.get("executor_id"),
            )
        )
        db.session.commit()
        return "", 201


@app.route("offers/<int: vid>", methods=["GET", "PUT", "DELETE"])
def offer(vid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(vid).to_dist()), 200, {'Content-Type': 'application/json; charset==utl-8'}
    if request.method == "PUT":
        offer_data = json.loads(request.data)
        new_data = Offer.query.get(vid)

        new_data.order_id = offer_data["order_id"]
        new_data.executor_id = offer_data["executor_id"]

        db.session.add(new_data)
        db.session.commit()
        return "", 201

    if request.method == "DELETE":
        delete_offer = Offer.query.get(vid)
        db.session.add(delete_offer)
        db.session.commit()
        return "", 204
