from pokedex.managers.analytics import  get_sum_user_agent
from flask_restful import Resource
class  User_Agent(Resource):
    def get(self):
        return get_sum_user_agent()
