from db import db
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin

class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('UserModel')