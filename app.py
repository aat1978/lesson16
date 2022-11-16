from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import raw_data
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    prise = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "prise": self.prise,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{Order.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))

    def to_dist(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


def init_database():
    db.drop_all()
    db.create_all()

    for user_data in raw_data.users:
        new_user = User(
            id=user_data.get("id"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            age=user_data.get("age"),
            email=user_data.get("email"),
            role=user_data.get("role"),
            phone=user_data.get("phone"),
        )
        db.session.add(new_user)
        db.session.commit()

    for order_data in raw_data.orders:
        new_order = Order(
            id=order_data.get("id"),
            name=order_data.get("name"),
            description=order_data.get("description"),
            start_data=order_data.get("start_data"),
            end_data=order_data.get("end_data"),
            address=order_data.get("address"),
            price=order_data.get("price"),
            customer_id=order_data.get("customer_id"),
            executor_id=order_data.get("executor_id"),
        )
        db.session.add(new_order)
        db.session.commit()

    for offer_data in raw_data.offers:
        new_offer = Offer(
            id=offer_data.get("id"),
            order_id=offer_data.get("order_id"),
            executor_id=offer_data.get("executor_id"),
        )
        db.session.add(new_offer)
        db.session.commit()


@app.route("/users", methods=["GET", "POST"])
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


@app.route("/users/<int:vid>", methods=["GET", "PUT", "DELETE"])
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


@app.route("/orders", methods=["GET", "POST"])
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


@app.route("/orders/<int:vid>", methods=["GET", "PUT", "DELETE"])
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


@app.route("/offers", methods=["GET", "POST"])
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


@app.route("/offers/<int:vid>", methods=["GET", "PUT", "DELETE"])
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


if __name__ == "__main__":
    init_database()
    app.run(host="localhost", port=5000, debug=True)
    
