from pokedex.models.pokemon import Generation, Ability,Type
from peewee import *
from playhouse.shortcuts import model_to_dict
def create_generation(name):
    return Generation.get_or_create(name=name)

def get_generations(query=None):
    generations=Generation.select(Generation.id,Generation.name)
    if  query !=None:
        generations= generations.where(query << Generation.name)
    return [dict(gen.get_small_data()) for gen in generations]

def number_of_abilities(generation_id):
    counter = len(Ability.select().where(Ability.generation_id == generation_id))
    return counter
def number_of_Types(generation_id):
   counter = len(Type.select().where(Type.generation_id == generation_id))
   print (counter)
   return counter
def add_number_of_abilities(liste):
    for p in liste:
        p["N_abilities"] = number_of_abilities(p["id"])
    print(liste)
    return liste

def add_number_of_types(liste):
    for p in liste:
        p["N_types"]=number_of_Types(p["id"])
        print(number_of_Types(p["id"]))
    print(liste)
    return liste

def get_generation(generation_name):
    generation,created = Generation.get_or_none(name = generation_name)
    return generation
