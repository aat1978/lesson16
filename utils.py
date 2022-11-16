import raw_data
from app import db
from user import User
from order import Order
from offer import Offer


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

