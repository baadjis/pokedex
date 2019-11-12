from flask import request
from flask_restful import Resource

from pokedex.managers.generations import add_number_of_types,add_number_of_abilities,get_generation,create_generation,get_generations
class Generations(Resource):
    def get(self):
        query = request.args.get("query")
        abilities = bool(request.args.get("abilities"))
        types = bool(request.args.get("types"))
        generations = list(get_generations(query))
        if abilities==True:
            generations=add_number_of_abilities(generations)
        if types == True:
            generations = add_number_of_types(generations)
        return generations

    def put(self):
         data= request.json
         return create_generation(data["name"])

class Generation(Resource):
    def get(self,generation_name):
        return get_generation(generation_name)
