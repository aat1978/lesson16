from app import db
from user import User
from order import Order


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{Order.__tablename__.id}"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__.id}"))

    def to_dist(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }
