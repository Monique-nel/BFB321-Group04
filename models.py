from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("Username", db.String, nullable=False)
    email = db.Column("Email", db.String, nullable=False)
    password = db.Column("Password", db.String, nullable=False)
    classification = db.Column("Classification", db.String, nullable=False)

