from flask import request
from flask_restful import Resource

from pokedex.errors import AbilityNotFoundError
from pokedex.managers.abilities import search_abilities, filter_ability_by_generation, add_effects


class Abilities(Resource):
    def get(self):
        bygeneration = bool(request.args.get("bygeneration"))
        effects = bool(request.args.get("effects"))
        limit = request.args.get("limit")
        offset = request.args.get("offset")
        query = request.args.get("query")
        data = search_abilities(query, limit, offset)
        if data is None:
            raise AbilityNotFoundError
        if effects == True:
            data = add_effects(data)
        if bygeneration == True:
            return filter_ability_by_generation(data)
        return data

    def post(self):
        pass
