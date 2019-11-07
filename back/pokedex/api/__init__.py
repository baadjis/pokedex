from time import strftime
from os import path,curdir
from flask import Blueprint
from flask_restful import Api
from flask import request,jsonify,Response

import dateparser
import geoip2.database


#geoippath=path.join(pathto,"GeoLite2-City-CSV","i")

from flask import Blueprint
from flask_restful import Api
from pokedex.models.database import db

from .pokemons import Pokemon, Pokemons,Stats
from .species import Species, Specie
from .types import Types
from .egg_groups import EggGroups
from .analytics import  User_Agent
from .users import Users, User, Buy, Matchs, Feed
from .potions import Potions

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

pathto=path.abspath("GeoLite2-City_20191022/GeoLite2-City.mmdb")
reader=geoip2.database.Reader(pathto)
def register_api(app):
    @api_bp.before_request
    def before_request():
        db.connect(reuse_if_open=True)

    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()


    api.add_resource(Pokemons, '/pokemons/')
    api.add_resource(Pokemon, '/pokemon/<pokemon_name>')
    api.add_resource(Types, '/types')
    api.add_resource(Species, '/species')
    api.add_resource(Specie, '/specie/<specie_id>')
    api.add_resource(EggGroups, '/egggroups')
    api.add_resource(User_Agent,'/analytics')
    api.add_resource(Stats,'/stats')
    api.add_resource(Users,'/users')
    api.add_resource(User,'/user/<user_id>')
    api.add_resource(Matchs,'/matchs')
    api.add_resource(Buy,'/buy')
    api.add_resource(Feed,'/feed/<user_id>')

    api.add_resource(Potions,'/potions')


    app.register_blueprint(api_bp, url_prefix="/api/v1")
