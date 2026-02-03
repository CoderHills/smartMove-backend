from app.extensions import db
from . import BaseModel

class Mover(BaseModel):
    __tablename__ = 'movers'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    service_area = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('mover', uselist=False))
