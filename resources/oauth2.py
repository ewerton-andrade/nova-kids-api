import time
from flask import request
from db import db
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import gen_salt
from flask_smorest import abort, Blueprint


from main.utils import query_by_model_field
from models.user import UserModel
from models.oauth2_client import OAuth2Client
from main.oauth2 import authorization, require_oauth

oauth2 = Blueprint('Oauth2_routes', __name__, description="Oauth Authentication")

def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

@oauth2.post('/create_client')
@require_oauth(['admin'])
def create_client():
    try:
        with require_oauth.acquire('profile') as token:
            if token:
                user = query_by_model_field(UserModel, 'id', token.user_id)
    except:
        abort(404, message="User not found.")

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)
    try:
        db.session.add(client)
        db.session.commit()
        return {"message": "Client was created"}, 201
    except:
        abort(504, "Client was not created")


@oauth2.post('/oauth/token')
def issue_token():
        return authorization.create_token_response()

@oauth2.post('/oauth/revoke')
def revoke_token():
    return authorization.create_endpoint_response('revocation')