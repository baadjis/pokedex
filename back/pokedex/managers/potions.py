import json

from  pokedex.models.potions import *
from peewee import *
def create_potion(name,restore,price,collection=False):
    potion=Potion.get_or_create(name = name ,restore = restore,price=price,collection=collection)
    return potion.get_small_data()
def get_potion_by_name(name):
    potion,created = Potion.get_or_none(name = name)
    return potion
def get_potions(query=None , bytype=False):
    matchingpotions = Potion.select()
    if query != None:
        query= query.lower()
        matchingpotions = matchingpotions.where(query << Potion.name)
    if bytype == True:
        matchingpotions = matchingpotions.group_by(Potion.collection)
    return json.dumps(model_to_dict(matchingpotions))
def delete_potion(potioname):
      return Potion.delete().where(Potion.name == potioname).execute()
