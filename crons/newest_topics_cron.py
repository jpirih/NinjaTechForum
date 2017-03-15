import datetime
from handlers.base import BaseHandler
from models.topic import Topic
from models.subscription import Subscription


class NewestTopics(BaseHandler):
    def get(self):
        newest_topics = Topic(Topic.updated_at < datetime.datetime.now() - datetime.timedelta(hours=24))
        #todo work in progress 
