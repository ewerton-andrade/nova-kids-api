import re
import logging
import calendar
import hashlib
from datetime import date, datetime, timedelta, time
from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity
from db import db

TOKEN_EXPIRATION_INTERVAL=timedelta(days=3)

def getCurrentTime():
    """
    Obs: O tempo para o sistema unix conta a partir de Janeiro 1, 1970, 00:00:00
    """
    return time.time()

def getDateHour(date:datetime):
    return date.hour

def getDateMinute(date:datetime):
    return date.minute

def getDateSecond(date:datetime):
    return date.second

def getWeekDay(date: datetime):
    return calendar.day_name[date.weekday()]

def retornaDataDia(data: datetime) -> str:
    return data.strftime("%d")

def retornaDataMes(data: datetime) -> str:
    return data.strftime("%m")

def retornaDataAno(data: datetime) -> str:
    return data.strftime("%Y")

def writeObject(dbObject):
    try:
        db.session.add(dbObject)
        db.session.commit()
    except:
        raise

def get_datetime_milisecs_pattern():
    return '%Y-%m-%d_%H-%M-%S-%f'

def is_past_day(d):
    return as_datetime(d) < now(coerceDateStart=True)

def as_date(d, pattern="%Y-%m-%d", coerceDateStart=False, coerceDateEnd=False):
    if not d:
        return None
    if not isinstance(d, date):
        d = datetime.strptime(d, pattern)
    if coerceDateStart:
        d = date_init(d)
    elif coerceDateEnd:
        d = date_end(d)
    return d

def datetime_to_timestamp(d, discard_milisecs=True):
    if d is None:
        return None
    d = as_datetime(d)
    t = d.timestamp()
    if discard_milisecs:
        return int(t)
    return t

def add_hours(d, hours, coerceDateStart=False, coerceDateEnd=False, to_date_string=False, to_timestamp=False):
    if not isinstance(d, date):
        d = as_date(d)
    d = d + timedelta(hours=hours)
    if coerceDateStart:
        d = date_init(d)
    elif coerceDateEnd:
        d = date_end(d)
    if to_date_string:
        d = as_date_string(d)
    elif to_timestamp:
        d = datetime_to_timestamp(d)
    return d

def trat_date_h(date, show_seconds=False, default_value = "-"):
    if date:
        return date.strftime("%Y-%m-%d %H:%M") if not show_seconds else date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return default_value

def date_init(d):
    """
    Parameter p can be a datetime, date, or a string in commonly accepted date formats.
    Returns a datetime whose time is the begining of the day from specified parameter.
    """
    if type(d) == str:
        d = datetime.strptime(d, "%Y-%m-%d")
    return datetime.combine(d, datetime.min.time())

def date_end(d):
    return datetime.combine(d, datetime.max.time())

def as_date_string(d, pattern='%Y-%m-%d'):
    if not d:
        return None
    return d.strftime(pattern)

def as_datetime_string(d, pattern=None):
    if not d:
        return None
    if pattern is None:
        pattern = get_datetime_milisecs_pattern()
    return d.strftime(pattern)

def now(delta_days=0, coerceDateStart=False, coerceDateEnd=False, to_date_string=False, to_datetime_string=False, string_format=None, to_date=False, to_timestamp=False):
    d = datetime.now()
    if delta_days != 0:
        d = d + timedelta(days=delta_days)
    if coerceDateStart:
        d = date_init(d)
    elif coerceDateEnd:
        d = date_end(d)
    if string_format is not None:
        return d.strftime(string_format)
    if to_date_string:
        return as_date_string(d)
    if to_datetime_string:
        return as_datetime_string(d)
    if to_date:
        return d.date()
    if to_timestamp:
        return d.timestamp()
    return d

def to_float(s, default_value=None, small=False):
    if s is None or s=='':
        return default_value
    try:
        s = float(s)
    except:
        return default_value
    if small and s >= 1E8:
        return default_value
    return s

def as_datetime(d, pattern="%Y-%m-%d-%H-%M-%S", accept_common_patterns=False):
    """
    - None or any object that evaluates to False will return None.
    - a datetime will return itself.
    - a date will be converted to a datetime with its minimum time value.
    - an int or float will be handled as a timestamp.
    - a number passed as string will be handled as a timestamp.
    - strings will be matched against common patterns in order to be parsed.
    """
    if not d:
        return None
    if isinstance(d, (int,float)):
        return datetime.fromtimestamp(d)
    if not isinstance(d, datetime):
        if isinstance(d, date):
            return datetime.combine(d, datetime.min.time())
        if isinstance(d, str):
            stamp = to_float(d)
            if stamp is not None:
                return datetime.fromtimestamp(stamp)
        if accept_common_patterns:
            d2 = str(d).replace(' ','T')  # simplify pattern matches below
            for p in [get_datetime_milisecs_pattern(), '%Y-%m-%d_%H-%M-%S', "%Y-%m-%d-%H-%M-%S", '%Y-%m-%dT%H:%M:%S']:
                try:
                    return datetime.strptime(d2, p)
                except: pass
        else:
            d = datetime.strptime(d, pattern)
    return d

def parse_datetime(stamp):
    return as_datetime(stamp, accept_common_patterns=True)

def is_date_string(d, pattern="%Y-%m-%d"):
    try:
        d = datetime.strptime(d, pattern)
        return d is not None
    except:
        return False
    
def is_datetime_string(d):
    try:
        return parse_datetime(d) is not None
    except:
        return False
    
def hours_to_seconds(hours):
    return hours * 60 * 60

def hash_pass(password):
    return hashlib.md5(password.encode()).hexdigest()

HTTP_SUCCESS                    = 200
HTTP_BAD_REQUEST                = 400
HTTP_UNAUTHORIZED               = 401
HTTP_FORBIDDEN                  = 403
HTTP_NOT_FOUND                  = 404
HTTP_CONFLICT                   = 409
HTTP_LOCKED                     = 423
HTTP_PRECONDITION_REQUIRED      = 428
HTTP_TOO_MANY_REQUESTS          = 429
HTTP_INTERNAL_SERVER_ERROR      = 500
HTTP_NOT_IMPLEMENTED            = 501
HTTP_COMMUNICATION_DISABLED     = 502  # Bad Gateway
HTTP_COMMUNICATION_UNAVAILABLE  = 503  # Service Unavailable

class MyCustomException(Exception):
    def __init__(self, message, code, report=False, custom_message_to_launch=None):
        super().__init__(message)
        self.message = message
        self.custom_message_to_launch = custom_message_to_launch
        self.code = code
        self.report = report
    def getMessageToLaunch(self):
        return self.custom_message_to_launch if self.custom_message_to_launch else self.message

def abort_missing_params(param_name=None, message=None, report=False, show_missing_param=False):
    if not message:
        message = f'missing: {param_name}' if param_name else 'missing params'
    raise MyCustomException(message, HTTP_BAD_REQUEST, custom_message_to_launch= None if show_missing_param else 'error', report=report)

def check_param(param, clean, param_name=None, show_invalid_param=False):
    if isinstance(param, list):
        for param_i in param:
            check_param(param_i, clean, param_name=param_name, show_invalid_param=show_invalid_param)
        return param
    if not isinstance(param, str):
        return param

    allowed_chars = allowed_chars_map.get(clean)
    if allowed_chars:  # rules based on restricted chars
        check_chars(param_name, param, allowed_chars)
        return param

    # clean 'simple' only does this. all other options usually do this plus additional rules
    for c in simple_forbidden_sql_tokens:
        if c in param:
            abort_invalid_parameter_value(param_name)

    if clean == 1:  # strict option: space, letters without accents, numbers, _ and -
        if not re.match("^[A-Za-z0-9_\-\s]*$", param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'state' or clean == 'city' or clean == 'city_or_state':  # clean=1 plus accented chars
        if not re.match("^[A-Za-z0-9_\-\sÀ-ÿ]*$", param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'address':  # clean=1 plus accented chars, and º ª \ / , . -
        if not re.match("^[A-Za-z0-9_\-\sÀ-ÿºª/\\\,\.()\-]*$", param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'node':  # letters, numbers, spaces, and the following symbols: _ - :
        if not re.match(r"^[A-Za-z0-9_:\- ]*$", param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'port':  # letters without accents, numbers, and following symbols: _ - / : .
        if not re.match("^[A-Za-z0-9_\-/:\.]*$", param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'mac':  # mac: letters, numbers, and : and _ . We are accepting _ because some screens use _ as placeholder for incomplete fields
        if not re.match("^[A-Za-z0-9:_]*$", param):
            abort_invalid_parameter_value(param_name, show_invalid_param=show_invalid_param)
    elif clean == 'date':
        if not is_date_string(param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'date_or_datetime':
        if not is_date_string(param) and not is_datetime_string(param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'alias':  # clean=1 plus accented chars and ( )
        if not re.match("^[A-Za-z0-9_\-\sÀ-ÿ()]*$", param):
            abort_invalid_parameter_value(param_name)
    elif clean == 'noncode':
        assert_noncode_param(param, param_name=param_name)

    return param

def assert_noncode_param(param, param_name=None, required=False):
    if param:
        p = str(param)
        chars = "<>{}()$#@%;|&*^~!?"
        for c in chars:
            if c in p:
                abort_invalid_parameter_value(param_name)
    elif required:
        abort_missing_params(param_name)
    return param

def abort_invalid_parameter_value(param_name=None, show_invalid_param=False):
    if show_invalid_param:
        raise MyCustomException(f'invalid: {param_name}' if param_name else 'invalid params', HTTP_BAD_REQUEST, report=True)
    else:
        _abort_hacking_attempt(f'invalid: {param_name}' if param_name else 'invalid params')

MAXIMUM_FORBIDDEN_ACTIONS_TO_BLOCK = 3
MAX_TIME_TO_WATCH_FORBIDDEN_ACTION_FOR_BLOCKING =hours_to_seconds(4)
ENABLE_PERMANENT_BLOCK = True


def _abort_hacking_attempt(message):
    e = prepare_abort_hacking_attempt(message)
    raise e

def get(param_name, default_value=None, required=False, clean='simple'):
    v = _get(param_name)
    if v is None or v == '':
        if required:
            abort_missing_params(param_name)
        return default_value
    if clean is not None:
        check_param(v, clean, param_name=param_name)
    return v

def get_int(param_name, default_value=None, required=False, multiply=None):
    v = _get(param_name)
    if v is not None and v != '':
        try:
            v = int(v)
        except ValueError:
            abort_invalid_parameter_value(param_name)
        if multiply is not None:
            v *= multiply
        return v
    if required:
        abort_missing_params(param_name)
    return default_value

def get_float(param_name, default_value=None, required=False, multiply=None):
    v = _get(param_name)
    if v is not None and v != '':
        try:
            v = float(v)
        except ValueError:
            abort_invalid_parameter_value(param_name)
        if multiply is not None:
            v *= multiply
        return v
    if required:
        abort_missing_params(param_name)
    return default_value

def get_boolean(param_name, default_value=False, required=False):
    try:
        if param_name in request.json:  #POST
            return bool(request.json[param_name])
    except:  # if request do not bring data as json, then request.json fails. let us check url params and form
        if param_name in request.values:
            v = request.values[param_name]
            return v==True or str(v).lower()=='true'
    if required:
        abort_missing_params(param_name)      
    return default_value

def _get(param_name):
    try:
        return request.json.get(param_name)
    except:  # if request do not bring data as json, then request.json fails. let us check url params and form
        if param_name in request.values:
            return request.values[param_name]
        if f'{param_name}[]' in request.values:
            return request.values.getlist(f'{param_name}[]')  # werkzeug.MultiDict
        return None
    
def get_login():
    try:
        token = get_jwt_identity()
        if token:
            return token.get('username')
    except:
        pass
    return None
    
allowed_chars_map = {
    'device_name' : set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-:/\\")  # letters, numbers, spaces, and the symbols _ - : \ /
}
simple_forbidden_sql_tokens = ["'", '"', "`", "\\", ";", "--", "/*", "*/"]

def check_chars(param_name, param, allowed_chars):
    for c in param:
        if c not in allowed_chars:
            abort_invalid_parameter_value(param_name)

def abort_invalid_parameter_value(param_name=None, show_invalid_param=False):
    if show_invalid_param:
        raise MyCustomException(f'invalid: {param_name}' if param_name else 'invalid params', HTTP_BAD_REQUEST, report=True)
    else:
        _abort_hacking_attempt(f'invalid: {param_name}' if param_name else 'invalid params')

##################### DB Functions #####################

def query_by_model_field(model, field_name, field_value):
    """
    Filter a Flask-SQLAlchemy model by a specific field.

    Args:
        model: Flask-SQLAlchemy model class.
        field_name: Name of the field to filter by.
        field_value: Value to filter against.

    Returns:
        List of model instances that match the filter criteria.
    """
    return model.query.filter(getattr(model, field_name) == field_value).all()[0]

# Function to delete a specific user by ID
def delete_record_by_field(model, field_name, field_value):
    register = query_by_model_field(model, field_name, field_value)
    if register:
        db.session.delete(register)
        db.session.commit()
        return True
    return False