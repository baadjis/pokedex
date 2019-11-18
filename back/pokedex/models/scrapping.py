from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db

class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'scrapping'


class Pokemon(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    numero=CharField()
    symbol = CharField()
    generation= CharField()

class Symbol(CommonModel):
    id =PrimaryKeyField
    character = CharField()
    color = CharField()
    meaning=CharField()
    description =CharField()

class Generation(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    years = CharField()
    titles = CharField()
    remakes = CharField()
    platforms = CharField()
    newpokemons = IntegerField()
    total=IntegerField()
with db:
    Pokemon.create_table(fail_silently=True)
    Symbol.create_table(fail_silently=True)
    Generation.create_table(fail_silently=True)
