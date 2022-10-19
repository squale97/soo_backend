#from flask import Flask
from cgi import print_exception
from traceback import print_exc
from flask import jsonify, request
from httplib2 import Credentials
from api import app, only_boutik, sook_response, basicAuthSession, only_admin, allowed
import datetime
from models import Account, Session, Product
import flask as fk
import hashlib



@app.route("/products", methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
#@only_admin(fk=fk)
def product_list():
    if request.method=="GET":
        credentials = basicAuthSession(fk.request)
        if credentials:
            products = Product.objects()
            produits= []
            for product in products:
                produits.append({"nom":product.nom, "description":product.description,
                "taille":product.taille, "prix":product.prix, "boutique":product.boutique, "categorie":product.categorie, "quantite":product.quantite})
            return sook_response(200, "succès", {"produits":produits})
        else:
            return sook_response(401, "erreur", {"title":"Information de sessio indisponible"})
    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})


@app.route("/add-product",  methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'] )

def add_product():
    if request.method=="POST":
        credentials = basicAuthSession(fk.request)
        if credentials:
            authorized, session = allowed(fk)
            if authorized:
                data = fk.request.get_json()
                if data:
                    nom = data["nom"]
                    description = data["description"]
                    boutique = data["boutique"]
                    prix = data["prix"]
                    taille = data["taille"]
                    categorie = data["categorie"]
                    quantite = data["quantite"]
                    product_add = Product(nom = nom, taille=taille, prix=prix,categorie=categorie, boutique=boutique, description=description, quantite=quantite)
                    product_add.save()
                    return sook_response(200, "succès", product_add.info())
                return sook_response(401, "erreur", {"title":"informations de produits indosponibles"})
            else:
                return sook_response(401, 'Opération Non Authorisée', "Session expirée. Vous devez vous reconnecter.")
        return sook_response(403, "erreur" ,{"title":"Opération non authorisée"})
    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})  


@app.route("/update-product/<id>",methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])  
def update_product(id):
    if request.method=="POST":
        credentials = basicAuthSession(fk.request)
        if credentials:
            authorized, session = allowed(fk)
            if authorized:
                update_product = Product.objects(id=id).first()
                data = fk.request.get_json()
                nom = data["nom"]
                description = data["description"]
                boutique = data["boutique"]
                prix = data["prix"]
                taille = data["taille"]
                categorie = data["categorie"]
                update_product.nom = nom
                update_product.description = description
                update_product.boutique = boutique
                update_product.prix = prix
                update_product.taille = taille
                update_product.categorie = categorie
                updated_at  = str(datetime.datetime.utcnow())
                update_product.updated_at = updated_at
                update_product.save()
            return sook_response(401, 'Opération Non Authorisée', "Session expirée. Vous devez vous reconnecter.")
        return sook_response(403, "erreur" ,{"title":"Opération non authorisée"})
    return sook_response(403, "erreur", {"title":"Cette interface n'accepte que la methode POST"})      