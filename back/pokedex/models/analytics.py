
from peewee import *

from .database import db


class CommonModel(Model):
    class Meta:
        database = db
        schema = 'analytics'


class SearchHistory(CommonModel):
    id = PrimaryKeyField()
    type = CharField()
    ip = CharField()
    search = CharField()

class User_Agent(CommonModel):
    id =PrimaryKeyField()
    search_id=ForeignKeyField(SearchHistory,backref="searchHistory")
    user_agent=CharField()
with db:
    SearchHistory.create_table(fail_silently=True)
    User_Agent.create_table(fail_silently=True)
