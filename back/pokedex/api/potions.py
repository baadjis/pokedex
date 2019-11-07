from flask import request
from flask_restful import Resource
from pokedex.managers.potions import get_potions,create_potion,delete_potion
class Potions(Resource):
    def get(self):
        query= request.args["query"]
        bytype= bool(request.args["bytype"])
        return get_potions(query,bytype)
    def post(self):
        data = request.json
        return (create_potion(data["name"] ,int(data["restore"]),int(data["price"]),bool(data["collection"])))

    def delete(self):
        query = request.args["name"]
        return(delete_potion(query))
