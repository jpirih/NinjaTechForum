import datetime
from handlers.base import BaseHandler
from models.comment import Comment


class DeleteCommentsCron(BaseHandler):
    def get(self):
        cureent_dt = datetime.datetime.now()
        month_older = datetime.timedelta(days=30)
        deleted_comments = Comment.query(Comment.deleted == True, Comment.updated_at < cureent_dt - month_older).fetch()

        for comment in deleted_comments:
            comment.key.delete()
