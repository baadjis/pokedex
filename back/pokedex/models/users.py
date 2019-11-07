import datetime

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
        schema = 'collections'
class Users(CommonModel):
     id = PrimaryKeyField()
     name = CharField()
     money = IntegerField(null=True,default=100)
     adde_at=DateTimeField(default=datetime.datetime.now)
     def get_small_data(self):
         return {"id":self.id,"name":self.name,"money":self.money,"adde_at":str(self.adde_at)}
class Pokemons(CommonModel):
   id =PrimaryKeyField()
   user_id= ForeignKeyField(Users,backref="user")
   name = CharField()
   hp = FloatField()
   special_attack = FloatField()
   defense = FloatField()
   attack = FloatField()
   special_defense = FloatField()
   speed = FloatField()

   @property
   def stats(self):
        return {'hp': self.hp, 'special-attack': self.special_attack, 'defense': self.defense, 'attack': self.attack,
                'special-defense': self.special_defense, 'speed': self.speed}

   def get_small_data(self):
        return {"id": self.id, "name": self.name, "stats": self.stats, 'sprite_back': self.sprite_back,
                'sprite_front': self.sprite_front}
   def set_stats(self,pokemon):
       pass
class Match(CommonModel):
    id =PrimaryKeyField()
    player1=ForeignKeyField(Users,backref="user1")
    player2=ForeignKeyField(Users,backref="user2")
    winner=ForeignKeyField(Users,backref="winner")
    duration= IntegerField()
    match_date = DateTimeField(default=datetime.datetime.now)

class Potions(CommonModel):
    id = PrimaryKeyField()
    name =CharField()
    user_id=ForeignKeyField(Users,backref="user")
    collection=BooleanField(default=False)


with db:
    Users.create_table(fail_silently=True)
    Pokemons.create_table(fail_silently=True)
    Match.create_table(fail_silently=True)
    Potions.create_table(fail_silently=True)

