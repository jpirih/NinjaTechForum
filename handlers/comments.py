from handlers.base import BaseHandler
from google.appengine.api import users
from helpers.decorators import validate_csrf, login_required
from models.comment import Comment
from models.topic import Topic
from models.user import User


class CreateCommentHandler(BaseHandler):
    @login_required
    @validate_csrf
    def post(self, topic_id):
        """ save new comment to database """
        user = User.logged_in_user()
        topic = Topic.get_by_id(int(topic_id))

        content = self.request.get('content')
        Comment.create(content, user, topic)
        return self.redirect_to('topic-details', topic_id=int(topic_id))



