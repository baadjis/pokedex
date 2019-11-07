from pokedex.models.analytics import SearchHistory,User_Agent
from peewee import*

def add_pokemon_search_history(ip, search,user_agent):

    history = SearchHistory.create(type='pokemon', ip=ip, search=search)
    Useragent=User_Agent.create(search_id=history.id,user_agent=user_agent)
    return (history,Useragent)
def get_sum_user_agent():
    query = (User_Agent
             .select(User_Agent.user_agent , fn.Count(SearchHistory.id).alias('count'))
             .join(SearchHistory, JOIN.LEFT_OUTER)
             .group_by(User_Agent))
    return [{"user_agent":p.user_agent,"count":p.count} for p in query]
