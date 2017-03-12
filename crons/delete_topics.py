import datetime
from handlers.base import BaseHandler
from models.topic import Topic


class DeleteTopicCron(BaseHandler):
    def get(self):
        deleted_topics = Topic.query(Topic.deleted == True,
                                     Topic.updated_at < datetime.datetime.now() - datetime.timedelta(days=30)).fetch()

        for topic in deleted_topics:
            topic.key.delete()