from flask_restful import Resource

from pokedex.managers.scrapping import get_pokemons_from_db, get_generations_from_db, get_symbols_from_db


class Scrappokemons(Resource):
    def get(self):
        return get_pokemons_from_db()


class Scrapgenerations(Resource):
    def get(self):
        return get_generations_from_db()


class Scrapsymbols(Resource):
    def get(self):
        return get_symbols_from_db()
