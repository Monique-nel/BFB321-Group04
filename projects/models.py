from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(150), nullable=False)
    trading_days = db.Column(db.String(100), nullable=True)
    trading_hours = db.Column(db.String(100), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)

    # Relationship: one user can own many markets
    markets = db.relationship('Market', backref='owner', lazy=True)
