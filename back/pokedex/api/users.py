from flask import request
from flask_restful import Resource

from pokedex.managers.users import get_user, user_pokemons, user_potions, add_user, update_user, search_users, \
    user_buy_potion, add_match_result, search_matchs, user_feed_pokemons_with_potion


class User(Resource):
    def get(self,user_id):
        user = get_user(int(user_id))
        p={"user":user.get_small_data()}
        if bool(request.args["pokemons"])==True:
            p["pokemons"]=user_pokemons(user)
        if bool(request.args["potions"]) ==True:
            p["potions"]=user_potions(user)
        print(p)
        return p
    def put(self,user_id):
        keys=request.args.keys()
        values= request.args.values()
        user=get_user(user_id)
        update_user(user ,keys,values)
        return user

class Users(Resource):
   def get(self):
       query=request.args['query']
       pokemons=bool(request.args["pokemons"])
       potions= bool(request.args["potions"])
       p=search_users(query,pokemons,potions)
       print (p)
       return p

   def post(self):
       data = request.json
       add_user(data["name"])

class Buy(Resource):
      def get(self,user_id):
          query = request.args["query"]
          user=get_user(int(user_id))
          return(user_buy_potion(user,query))

class Matchs(Resource):
    def get(self):
        user=request.args["user"]
        query=bool(request.args["query"])
        return search_matchs(user,query)
    def post(self):
        player1 = get_user(int(request.args["player1"]))
        player2 = get_user(int(request.args["player2"]))
        return (add_match_result(player1, player2))

class Feed(Resource):
      def post(self,user_id):
          user= get_user(user_id)
          potionname=request.args["potion"]
          pokemon= request.args.get("pokemons")
          pokemon= int(pokemon) if pokemon else None
          return user_feed_pokemons_with_potion(user,potionname,pokemon)
