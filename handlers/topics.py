from handlers.base import BaseHandler
from helpers.tools import LOGIN_MESSAGE
from helpers.decorators import validate_csrf
from google.appengine.api import users

from models.comment import Comment
from models.topic import Topic


class CreateTopicHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            return self.render_template_with_csrf('topics/topic_new.html')
        else:
            message = LOGIN_MESSAGE
            params = {"message": message}
            return self.render_template('topics/topic_new.html', params=params)

    @validate_csrf
    def post(self):
        user = users.get_current_user()
        if user:
            title = self.request.get('title')
            content = self.request.get('content')

            # add new topic
            new_topic = Topic(title=title, content=content, author_email=user.email())
            new_topic.put()
            return self.redirect_to('main-page')
        else:
            # login required message
            message = LOGIN_MESSAGE
            params = {'message': message}
            return self.render_template('error.html', params=params)


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        # topic details and topic comments
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == int(topic_id)).order(Comment.created_at).fetch()

        parms = {'topic': topic, 'comments': comments}
        return self.render_template_with_csrf('topics/topic_details.html', params=parms)

