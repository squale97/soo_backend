import datetime

import json
import time

from flask_mongoengine import MongoEngine
db = MongoEngine()

class Session(db.Document):
    """Identity backend session model.
    The model holding the account information.

    Attributes:
        code: The account user name.
        status: The account status [created, online, offline, locked, archived].
        created_at: When the session was created.
        updated_at: When the session was updated.
        key: The account session key.
        extend: A dictionary of to add other fields to the session model.
    """
    code = db.StringField()
    credit = db.StringField()
    status_group = ["created", "online", "offline", "locked", "archived"]
    status = db.StringField(default="created", choices=status_group)
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    updated_at = db.StringField(default=None)
    changed_at = db.StringField(default=None)
    key = db.StringField(default=None)
    
    extend = db.DictField()

  
    
    def info(self):
       
       
        data = {}
        data["code"] = self.code
        data["status"] = self.status
        data["changed-at"] = self.changed_at
        data["key"] = self.key
        return data


"""
class Session_History(db.Document):
    Identity history backend session model.
    The model holding changes to the session information.

    Attributes:
        changed_at: When the account was changed.
        code: The account user name.
        status: The account status [created, online, offline, locked, archived].
        changed_at: When the account was changed.
        key: The account session key.
    
    code = db.StringField(default=None)
    status_group = ["created", "online", "offline", "locked", "archived"]
    status = db.StringField(default="created", choices=status_group)
    changed_at = db.StringField(default=str(datetime.datetime.utcnow()))
    key = db.StringField(default=None)

    extend = db.DictField()

    def prepare(self, current):
        self.code = current.code
        self.status = current.status
        self.key = current.key
        self.extend = current.extend

    def freeze(self, changed):
        track = 0
        if self.code != changed.code:
            track += 1
        if self.status != changed.status:
            track += 1
        if self.key != changed.key:
            track += 1
        if self.extend != changed.extend:
            track += 1
        if track > 0:
            self.save()

    def info(self):
        A based dictionary compact of the fields.

        Returns:
          The augmented dictionary.
        
        data = {}
        data["code"] = self.code
        data["status"] = self.status
        data["changed-at"] = self.changed_at
        data["key"] = self.key

        return data

    def extended(self):
        Allow extension without migration.

        Returns:
          The augmented dictionary.
        
        data = self.info()
        data['extend'] = self.extend
        return data

    def to_json(self):
        Transform the extended dictionary into a pretty json.

        Returns:
          The pretty json of the extended dictionary.
        
        data = self.extended()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
"""