from flask.json import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import Blueprint, abort
from datetime import timedelta, datetime
from main.utils import get, hash_pass, now, trat_date_h, add_hours, query_by_model_field , HTTP_UNAUTHORIZED
from models.user import UserModel


services = Blueprint("Services", __name__ , description="API Services")

@services.route('/login', methods=["POST"])
def login():
    response,code = doLogin()
    return jsonify(response),code

def generate_user_token(values):
    token = create_access_token(values)
    token = 'Bearer ' + (token.decode() if isinstance(token, bytes) else token)
    return token

def generate_user_refresh_token(values):
    token = create_refresh_token(values)
    token = 'Bearer ' + (token.decode() if isinstance(token, bytes) else token)
    return token

def get_expiration_date_token():
    date = None
    TOKEN_EXPIRATION_INTERVAL = timedelta(days=3)
    if TOKEN_EXPIRATION_INTERVAL.seconds > 0: #For testing, where the expiration time should be low. Expiration warning is given 1min before token expires
        date_aux = now(string_format='%Y-%m-%d %H:%M:%S')
        date = trat_date_h(add_hours(datetime.strptime(date_aux, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=TOKEN_EXPIRATION_INTERVAL.seconds/60), hours=(-1/60)), show_seconds=True)
    elif TOKEN_EXPIRATION_INTERVAL.days > 0:
        date = trat_date_h(add_hours(now(delta_days=TOKEN_EXPIRATION_INTERVAL.days), hours=-1), show_seconds=True) #Expiration warning is given 1 hour before token expires
    return date

def doLogin():
    email = get('username', required=True)
    password_received = get('password', required=True)
    user, user_status, ok = _search_user(UserModel, email, password_received)
    if not ok:
        return user, user_status
    return {'token': generate_user_token(user), 'refresh_token': generate_user_refresh_token(user),'expiration_date': get_expiration_date_token(), **user}, user_status

def _search_user(userModel:UserModel, email, password) -> UserModel:
    password_md5 = hash_pass(password)
    user = query_by_model_field(userModel,'username', email)
    if not user or not user.check_password(user.password, password_md5):
        return abort(HTTP_UNAUTHORIZED, message="Invalid login or password")
    response = { 'email': user.username, 'profile': user.profile, 'owner': user.provider}
    return response, 200, True
