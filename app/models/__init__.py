from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Import all models here
from .user import User
from .mover import Mover
from .address import Address
from .booking import Booking
from .review import Review
from .inventory import Inventory
from .chat import Message
from .notification import Notification
from .quote import Quote
