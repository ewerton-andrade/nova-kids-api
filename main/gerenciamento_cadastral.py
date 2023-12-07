import hashlib

from main.utils import abort_invalid_parameter_value

HOMOLOG_PROFILE = 'homolog'
READ_PROFILE = 'read'
REGULAR_PROFILE = 'regular'
BETA_PROFILE = 'beta'
MANAGER_PROFILE = 'manager'
ADMIN_PROFILE = 'admin'

def check_valid_profile(profile):
    profiles = [HOMOLOG_PROFILE, READ_PROFILE, REGULAR_PROFILE, BETA_PROFILE, MANAGER_PROFILE, ADMIN_PROFILE ]


# def create_web_user(user_model, email, password, profile):
#     ### Colocar aqui uma função que extraia a informacao do perfil do usuario baseado no token jwt
#     if len(password) < 6:
#         abort_invalid_parameter_value('password too short')
#     user['email'] = email
#     user['password'] = hashlib.md5(password.encode()).hexdigest()
#     user['profile'] = profile if check_valid_profile(profile) else abort_invalid_parameter_value(param_name='profile')
#     # web_user['provider'] = get_owner()
#     # df_web_user.append(web_user)
#     # df_web_user = pd.DataFrame(df_web_user)
#     try:
#         connection = util.get_connection_wrapper()
#         db.write_db("webuser", df_web_user, con=connection, update_conflict_attributes=['email'], force_uniqueness=True)
            
#     except sqlalchemy.exc.IntegrityError:
#         abort_conflict()
#     except ValueError:
#         abort_missing_params()