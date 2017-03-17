from handlers.base import BaseHandler
from helpers.messages import COMMENT_AUTHOR
from helpers.tools import show_info_page

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


class DeleteCommentHandler(BaseHandler):

    def post(self, comment_id):
        """ soft delete for comments only by author or admin """
        comment = Comment.get_by_id(int(comment_id))
        user = User.logged_in_user()

        if User.is_admin(user) or User.is_author(user, comment):
            Comment.delete(comment)
            return self.redirect_to("topic-details", topic_id=comment.topic_id)
        else:
            return show_info_page(message=COMMENT_AUTHOR)



