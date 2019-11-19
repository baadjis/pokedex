from os import path

import geoip2.database
from flask import Blueprint
from flask_restful import Api

from pokedex.api.abilities import Abilities
from pokedex.api.generations import Generations, Generation
from pokedex.api.scrapping import Scrappokemons, Scrapgenerations, Scrapsymbols
from pokedex.errors import NotFoundError
from pokedex.models.database import db
from .analytics import User_Agent
from .egg_groups import EggGroups
from .pokemons import Pokemon, Pokemons, Stats
from .potions import Potions
from .species import Species, Specie
from .types import Types
from .users import Users, User, Buy, Matchs, Feed

# geoippath=path.join(pathto,"GeoLite2-City-CSV","i")

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

pathto = path.abspath("GeoLite2-City_20191022/GeoLite2-City.mmdb")
reader = geoip2.database.Reader(pathto)


def register_api(app):
    @api_bp.before_request

    def before_request():
        db.connect(reuse_if_open=True)

    """close the database after any request"""

    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()

    """this function handle error from  request"""

    @api_bp.errorhandler(NotFoundError)
    def if_not_found(error):
        response = {"error": f"{error.resource} {error.resource_id} not found"}
        return response, 404

    """add resources"""
    api.add_resource(Pokemons, '/pokemons/')
    api.add_resource(Pokemon, '/pokemon/<pokemon_name>')
    api.add_resource(Types, '/types')
    api.add_resource(Species, '/species')
    api.add_resource(Specie, '/specie/<specie_id>')
    api.add_resource(EggGroups, '/egggroups')
    api.add_resource(User_Agent, '/analytics')
    api.add_resource(Stats, '/stats')
    api.add_resource(Users, '/users')
    api.add_resource(User, '/user/<user_id>')
    api.add_resource(Matchs, '/matchs')
    api.add_resource(Buy, '/buy')
    api.add_resource(Feed, '/feed/<user_id>')
    api.add_resource(Abilities, '/abilities')
    api.add_resource(Potions, '/potions')
    api.add_resource(Generations, '/generations')
    api.add_resource(Generation, '/generation/<generation_name>')
    api.add_resource(Scrappokemons, '/scrappokemons')
    api.add_resource(Scrapgenerations, '/scrapgenerations')
    api.add_resource(Scrapsymbols, '/scrapsymbols')

    app.register_blueprint(api_bp, url_prefix="/api/v1")
