import json
import time

from peewee import *
from playhouse.shortcuts import model_to_dict

from pokedex.models.users import Users, Pokemons, Potions, Match
from pokedex.managers.pokemons import get_pokemon_by_name
from pokedex.managers.potions import get_potion_by_name
from copy import deepcopy
def get_user(user_id):
    return Users.get_or_none(user_id)

def add_user(name):
    user, created = Users.get_or_create(name=name)
    return (user,created)
def user_add_pokemon(user,pokemonname):
    pokemon=get_pokemon_by_name(pokemonname)
    stats=pokemon.stats
    pok = Pokemons.create(user_id=user.id,**stats)
    return pok
def delete_pokemon(pokemon):
   p = pokemon.delete_instance(recursive=True)
   return p
def delete_potion(potion):
    p=potion.delete_instance(recursive=True)
    return p
def update_pokemon_stat(pokemon,stat,value):
    update = {stat:value}
    p = Pokemons.update(**update).where(Pokemons.id==pokemon).execute()
    return p
def update_user(user,keys,values):
    update=dict(zip(keys,values))
    p=Users.update(**update).where(id==user.id).execute()
    return p
def user_pokemons(user):
    query= (Pokemons.select().where(Pokemons.user_id == user)
            .order_by(Pokemons.hp))
    return query
def user_buy_potion(user,potionname):
    potion = get_potion_by_name(potionname)
    available_money=int(user.money) - int(potion.price)
    if available_money >= 0:
        p = Potions.create(name=potionname,user_id=user.id)
        u = update_user(user,"money",available_money)
        return (p,u)
def user_potion_names(user):
    userpotionsnames= set([potion.name for potion in user_potions(user)])
    return userpotionsnames

def user_potions(user):
    query = (Potions.select().where(Potions.user_id == user))
    return query
def user_feed_pokemons_with_potion(user,potionname,pokemonid):
    pokemonstofeed =user_pokemons(user)
    userpotions =user_potion_names(user)
    user_potions_of_thisname = [potion for potion in userpotions if (potion.name == potionname)]
    if (len(user_potions_of_thisname)>0) :
        potion = get_potion_by_name(potionname)
        if (potion.collection == True) :
          for poke in pokemonstofeed:
            potion = get_potion_by_name(potionname)
            newhp = int(poke.hp)+ int(potion.restore)
            update_pokemon_stat(poke,'hp',newhp)
          delete_potion(user_potions_of_thisname[0].id)
          return pokemonstofeed
        else:
            if pokemonid!=None:
             pokemon=Pokemons.get(Pokemons.id == pokemonid)
             potion = get_potion_by_name(potionname)
             newhp = int(pokemon.hp) + int(potion.restore)
             update_pokemon_stat(pokemon, 'hp', newhp)
             delete_potion(user_potions_of_thisname[0].id)
             return pokemon



def pokemon_attack(pokemon,other):
    dommage=max(0,int(pokemon.attack)-int(other.defense))
    return dommage

def fight(pokemon1,pokemon2):
    hp1=int(pokemon1.hp)
    hp2=int(pokemon2.hp)
    i=1
    while (min(hp1,hp2)> 0):
        domage =pokemon_attack(pokemon1,pokemon2)
        hp2= max(0,hp2-domage)
        if (i%2==0):
            domage=pokemon_attack(pokemon2,pokemon1)
            hp1 = max(0, hp1 - domage)
        i+=1

    if (hp1 == 0):
        delete_pokemon(pokemon1)
        update_pokemon_stat(pokemon2,'hp',hp2)
        return pokemon2
    else:
        delete_pokemon(pokemon2)
        update_pokemon_stat(pokemon1,'hp',hp1)
        return pokemon1

def create_Match(liste1,liste2):
    startime= time.time()
    if len(liste1) == 0:
        return (liste2,time.time() - startime)

    if len(liste2) == 0:
        return (liste2,time.time() - startime)
    winner = fight(liste1[0],liste2[0])
    if winner == liste1[0]:
        return create_Match(liste1,liste2[1:])
    else:
       return create_Match(liste2,liste1[1:])

def add_match_result(user1,user2):
     result=create_Match(user_pokemons(user1),user_pokemons(user2))
     duration =result[0]
     winner= user2.id if (len(user_pokemons(user1))==0) else user1.id
     return(Match.create(player1=user1,player2=user2,winner=winner,duration=duration))
def search_users(query=None,pokemons=False,potions=False):
     users=Users.select()
     if query != None:
         query= query.lower()
         users= users.where(query << Users.name)
     if pokemons==True:
         users=users.join(pokemons)
     if potions == True:
         users=users.join(potions)
     return json.dumps(model_to_dict(users))

def search_matchs(user=None ,winner=False):
    matchingmatchs=Match.select().join(Users)
    if user !=None:
        if winner ==True:
           matchingmatchs= matchingmatchs.where(Match.winner==user)
        else:
            matchingmatchs=matchingmatchs.where((Match.player1 == user) or (Match.player2 == user))
    return json.dumps(model_to_dict(matchingmatchs))



