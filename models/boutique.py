
import json
import datetime

from flask_mongoengine import MongoEngine
#db.create_all()
db = MongoEngine()

class Boutique(db.Document):
    #id = db.Column(db.Integer(), primary_key=True)
    nom = db.StringField()
    description= db.StringField()
    
    image = db.FileField()
    
    created_at = db.StringField()
    updated_at = db.StringField()
    categorie = db.StringField()



    extend = db.DictField()

    

    def info(self):
        
        data = {}
        data["nom"] = self.nom
    
        data["description"] = self.description
        
        
        data["updated-at"] = self.updated_at
        data["created_at"] = self.created_at
        data["categorie"] = self.categorie

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