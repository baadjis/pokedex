from flask import request
from flask_restful import Resource
from pokedex.managers.analytics import add_pokemon_search_history

from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon,get_pokemon_form ,get_moyenne


class Pokemons(Resource):
    def get(self):
        query = request.args.get('query')
        typo = request.args["type"]
        limit = int(request.args["limit"])
        print(typo)
        print(query)
        forms= bool(request.args["forms"])
        pokemons_matching = search_pokemons(query, typo,limit)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]
        if forms == True:
            pokemons =[{"pokemons":pokemon.get_small_data(),"forms":get_pokemon_form(pokemon)} for pokemon in pokemons_matching]
        useragent= request.user_agent
        add_pokemon_search_history(request.remote_addr, query,useragent)

        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        forms=bool(request.args["forms"])
        if pokemon is None:
            return {'msg': 'Not found'}, 404
        if forms == True:
            return {"stats":pokemon.get_small_data(),"forms":get_pokemon_form(pokemon)}
        return pokemon.get_small_data()

    def patch(self, pokemon_name):
        return 'panic', 500

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result
class Stats(Resource):
    def get(self):
        return get_moyenne()
