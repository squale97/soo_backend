
import json
import datetime

from flask_mongoengine import MongoEngine
#db.create_all()
db = MongoEngine()

class Account(db.Document):
    #id = db.Column(db.Integer(), primary_key=True)
    email = db.StringField()
    password = db.StringField()
    nom = db.StringField()
    prenom = db.StringField()
    numero = db.StringField()
    password = db.StringField()
    address = db.StringField()
    scope_group = ["admin", "user", "boutiquier"]
    scope = db.StringField(default="user", choices=scope_group)
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    updated_at = db.StringField(default=None)



    extend = db.DictField()

    def is_minimal(self):
        """Check for minimal fields.

        Returns:
            outcome of the check.
        """
        if self.username or self.password or self.scope:
            return True
        else:
            return False

    def info(self):
        
        data = {}
        data["email"] = self.email
        data["numero"] = self.numero
        data["nom"] = self.nom
        data["prenom"] = self.prenom
        data["address"] = self.address
        data["scope"] = self.scope
        data["updated-at"] = self.updated_at
        data["created_at"] = self.created_at

        return data

    def extended(self):
        """Allow extension without migration.

        Returns:
            The augmented dictionary.
        """
        data = self.info()
        data['extend'] = self.extend
        return data

def to_json(self):
    """Transform the extended dictionary into a pretty json.

    Returns:
        The pretty json of the extended dictionary.
    """
    data = self.extended()
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))