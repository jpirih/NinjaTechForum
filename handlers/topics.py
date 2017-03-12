from handlers.base import BaseHandler
from helpers.decorators import validate_csrf, login_required
from google.appengine.api import users

from models.comment import Comment
from models.topic import Topic
from models.user import User


class CreateTopicHandler(BaseHandler):
    @login_required
    def get(self):
        """ create topic form view """
        return self.render_template_with_csrf('topics/topic_new.html')

    @login_required
    @validate_csrf
    def post(self):
        """ save new topic  to datastore """
        user = User.logged_in_user()

        title = self.request.get('title')
        content = self.request.get('content')

        # add new topic
        Topic.crate(title=title, content=content, author=user)

        return self.redirect_to('main-page')


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        """ topic details and topic related comments """

        user = User.logged_in_user()

        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == int(topic_id)).order(Comment.created_at).fetch()

        parms = {'topic': topic, 'comments': comments, 'user': user}
        return self.render_template_with_csrf('topics/topic_details.html', params=parms)


class DeleteTopicHandler(BaseHandler):
    @login_required
    def post(self, topic_id):
        """ topic soft delete hahdler only by author or admin """
        topic = Topic.get_by_id(int(topic_id))
        user = User.logged_in_user()
        if User.is_admin(user) or User.is_author(user, topic):
            Topic.delete(topic)
            return self.redirect_to('main-page')
        else:
            return self.write('only author or admin can delete topic')



