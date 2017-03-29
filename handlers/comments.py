from handlers.base import BaseHandler
from helpers.messages import COMMENT_AUTHOR, ADMIN_RELOAD, ADMIN_ACCESS

from helpers.decorators import validate_csrf, login_required
from models.comment import Comment
from models.topic import Topic
from models.user import User


# Show all comments
class CommentsListHandler(BaseHandler):
    @login_required
    def get(self):
        user = User.logged_in_user()
        if User.is_admin(user):
            comments  = Comment.query(Comment.deleted == False).order(-Comment.created_at).fetch()
            params = {"comments": comments}
            return self.render_template_with_csrf("comments/comments_list.html", params=params)
        else:
            return self.render_template("error.html", params={"message": ADMIN_ACCESS})

# create new comment
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


# edit comment
class EditCommentHandler(BaseHandler):
    @login_required
    @validate_csrf
    def post(self, comment_id):
        """ Edit comment by author or forum administrator """
        commment = Comment.get_by_id(int(comment_id))
        user = User.logged_in_user()

        if User.is_admin(user) or User.is_author(user, commment):
            content = self.request.get("content")
            Comment.update(commment, content)
            return self.redirect_to("topic-details", topic_id=int(commment.topic_id))
        else:
            return self.render_template("error.html", params={"message": COMMENT_AUTHOR})


# delete comment -soft delete
class DeleteCommentHandler(BaseHandler):
    @login_required
    @validate_csrf
    def post(self, comment_id):
        """ soft delete for comments only by author or admin """
        comment = Comment.get_by_id(int(comment_id))
        user = User.logged_in_user()

        if User.is_admin(user) or User.is_author(user, comment):
            Comment.delete(comment)
            return self.redirect_to("topic-details", topic_id=comment.topic_id)
        else:
            return self.render_template("error.html", params={"message": COMMENT_AUTHOR})


# reload comment - undo soft delete
class ReloadCommentHandler(BaseHandler):

    @login_required
    @validate_csrf
    def post(self, comment_id):
        """ comment  reload hahdler only by admin """
        comment = Comment.get_by_id(int(comment_id))
        user = User.logged_in_user()
        if User.is_admin(user):
            Comment.reload(comment)
            return self.redirect_to('topic-details', topic_id=int(comment.topic_id))
        else:
            return self.render_template("error.html", params={"message": ADMIN_RELOAD})


# destroy comment -> delete comment completely from datastore
class DestroyCommentHandler(BaseHandler):
    @login_required
    @validate_csrf
    def post(self, comment_id):
        """ Destroy comment delete comment completely from datastore """
        comment = Comment.get_by_id(int(comment_id))
        user = User.logged_in_user()
        if User.is_admin(user):
            Comment.destroy(comment)
            return self.redirect_to("deleted-comments-list")
        else:
            return self.render_template("error.html", params={"message": ADMIN_ACCESS})


# Deleted comments list handler
class DeletedCommentsListHandler(BaseHandler):
    @login_required
    def get(self):
        """ list of all deleted topics  to completely delete or renew admin only """
        user = User.logged_in_user()

        if User.is_admin(user):
            comments = Comment.query(Comment.deleted == True).fetch()
            params = {"comments": comments}
            return self.render_template_with_csrf("comments/comments_deleted_list.html", params=params)
        else:
            return self.render_template("error.html", params={"message": ADMIN_ACCESS})



