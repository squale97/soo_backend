#from flask import Flask
from flask import request
from api import app, sook_response, basicAuthSession, only_admin
import datetime
from models import Account, Session
import flask as fk
import hashlib

def login(fk):
    credentials = basicAuthSession(fk.request)
    if credentials is None:
        return None
    else:
        username = credentials.username
        password = credentials.password
        hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
        account = Account.objects(numero=username, password=hashed_password).first()
        if account:
            session = Session.objects(code=str(account.id)).first()
            if session is None:
                session = Session(code=str(account.id))

            now = str(datetime.datetime.utcnow())
            session.key = hashlib.sha256(('digiSookSession_%s_%s'%(str(account.id), now)).encode("ascii")).hexdigest()
            session.status = "online"
            session.updated_at = now
            session.save()
            return session
        else:
            return None


@app.route('/register', methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
def register():

    if request.method == "POST":
        data = request.get_json()
        if data:
            nom = data["name"]
            prenom = data["prenom"]
            number = data["numero"]
            addresse = data["address"]
            password = data["password"]
            hashpass = hashlib.sha256((password).encode("ascii")).hexdigest()
            email = data["email"]
            scope = data["scope"]
            check_account = Account.objects(numero=number).first()
            if check_account:
                return sook_response(402, "erreur", {"title":"Ce numero existe déja"})
            account = Account(nom=nom, prenom=prenom, numero=number,
                        address=addresse, password=hashpass, email=email, scope=scope)
        
            account.save()
    
            return sook_response(200, "success", account.info())
        else:
            return sook_response(401, "erreur", {"title":"inforamtions manquantes"},)
    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})


@app.route('/login', methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
def login_account():
    
    if request.method=="GET":
        session = login(fk)
        if session:
            account = Account.objects(id=session.code).first()
            #details = Info.objects(code=session.code).first()
            info = session.info()
            info['account'] = account.info()
            #del info['account']['code']
            #if details:
                #info['details'] = details.info()
                #del info['details']['code']
            return sook_response(200, f'Vous êtes connecté', info)
        else:
            return sook_response(401, 'Opération Non Authorisée', "Accès refusé.")
        

        

    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})




@app.route("/update-account", methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
def update_account():
    if fk.request.method=="POST":
        credentials = basicAuthSession(fk.request)
        if credentials:
            data= fk.request.get_json()
            if data:
                old_number = data["old_number"]
                number = data["number"]
                password = data["password"]
                address = data["address"]
                account = Account(numero=old_number).first()
                if account:
                    account.numero=number
                    account.password=password
                    account.address = address
                    return sook_response(200, "succèss", account.info())
                return sook_response(401, "erreur", {"title":"compte inexistant"})
            return sook_response(401, "erreur",{"title":"informations non disponibles"})
        return sook_response(401, "erreur",{"title":"opération non authorisée"})

    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})






@app.route("/accounts", methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
@only_admin(fk=fk)
def account_list():
    if request.method=="GET":
        credentials = basicAuthSession(fk.request)
        if credentials:
            accounts = Account.objects()
            accounts_list= []
            for account in accounts:
                print(account.info())
                accounts_list.append(account.info())
            return sook_response(200, "succès", {"account_list":accounts_list})
        else:
            return sook_response(401, "erreur", {"title":"Information de sessio indisponible"})
    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})
