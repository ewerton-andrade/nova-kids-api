from db import db
from datetime import datetime 

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(15), unique=False, nullable=False)
    provider = db.Column(db.String(15), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id}>'
    
    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password, hashpass):
        return password == hashpass