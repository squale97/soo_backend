
import flask as fk
from flask import Flask
from werkzeug.http import parse_authorization_header
import json
import hashlib
from models import Account, Session
from functools import update_wrapper
app = Flask(__name__)


#def testFunction():
    #return "test ok"
def allowed(fk):
    credentials = basicAuthSession(fk.request)
    if credentials is None:
        return False, None
    else:
        key = credentials.username
        session = Session.objects(key=key, status__in=['online']).first()
        if session:
            return True, session
        else:
            return False, None


def has_admin():
    admin = Account.objects(scope='admin').first()
    if admin is not None:
        return True
    else:
        return False

      
def sook_response(code, title, content):
    response = {'code':code, 'title':title, 'content':content}
    return fk.Response(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')), status=code, mimetype='application/json')


def basicAuthSession(request):
    """Extract the authorization content from the header.

    Returns:
      the password if found and None if not.
    """

    result = parse_authorization_header(request.headers.get('authorization'))
    if result:
        return result
    else:
        return None


def only_admin(fk=None, max_age=21600, attach_to_all=True, automatic_options=True):
    """Impose that the endpoint be accessible only to the admin account.
    A valid admin session key must be available.

    Returns:
      Allow in or return a 401 or 403.
    """

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and fk.request.method == 'OPTIONS':
                resp = app.make_default_options_response()

            if not has_admin():
                return sook_response(555, 'Opération Non Authorisée', {"message": "Compte administrateur inexistant. Vous devez le configuer."})
            else:
                authorized, session = allowed(fk)

                credentials = basicAuthSession(fk.request)
                if credentials is None:
                    session_key = None
                else:
                    session_key = credentials.username

                if authorized:
                    account = Account.objects(id=session.code, scope="admin").first()
                    if account is not None:
                        return fk.make_response(f(*args, **kwargs))
                    else:
                        return sook_response(401, 'Opération Non Authorisée', "Seul un administrateur peut y accéder.")
                elif session_key is None:
                    return sook_response(403, 'Opération Non Authorisée', "Information de session indisponible.")
                else:
                    return sook_response(401, 'Opération Non Authorisée', "Session expirée. Vous devez vous reconnecter.")

        return update_wrapper(wrapped_function, f)
    return decorator






def only_boutik(fk=None, max_age=21600, attach_to_all=True, automatic_options=True):
    """Impose that the endpoint be accessible only to the admin account.
    A valid admin session key must be available.

    Returns:
      Allow in or return a 401 or 403.
    """

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and fk.request.method == 'OPTIONS':
                resp = app.make_default_options_response()

            if not has_admin():
                return sook_response(555, 'Opération Non Authorisée', {"message": "Compte administrateur inexistant. Vous devez le configuer."})
            else:
                authorized, session = allowed(fk)

                credentials = basicAuthSession(fk.request)
                if credentials is None:
                    session_key = None
                else:
                    session_key = credentials.username

                if authorized:
                    account = Account.objects(id=session.code, scope="boutiquier").first()
                    if account is not None:
                        return fk.make_response(f(*args, **kwargs))
                    else:
                        return sook_response(401, 'Opération Non Authorisée', "Seul un administrateur peut y accéder.")
                elif session_key is None:
                    return sook_response(403, 'Opération Non Authorisée', "Information de session indisponible.")
                else:
                    return sook_response(401, 'Opération Non Authorisée', "Session expirée. Vous devez vous reconnecter.")

        return update_wrapper(wrapped_function, f)
    return decorator


