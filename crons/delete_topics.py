import datetime
from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic


class DeleteTopicCron(BaseHandler):
    def get(self):
        deleted_topics = Topic.query(Topic.deleted == True,
                                     Topic.updated_at < datetime.datetime.now() - datetime.timedelta(days=30)).fetch()

        for topic in deleted_topics:
            comments = Comment.query(Comment.topic_id == topic.key.id()).fetch()
            for comment in comments:
                comment.key.delete()
            topic.key.delete()
