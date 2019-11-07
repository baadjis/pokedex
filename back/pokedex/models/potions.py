from  peewee import *
from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db
from .pokemon import Pokemon
class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)
    class Meta:
        database = db
        schema = 'consommables'
class Potion(CommonModel):
    id =PrimaryKeyField()
    name = CharField()
    restore = IntegerField(null=False)
    collection = BooleanField(default=True)
    price =IntegerField(null=False)
with db:
    Potion.create_table(fail_silently=True)
