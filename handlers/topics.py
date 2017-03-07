from handlers.base import BaseHandler
from helpers.tools import LOGIN_MESSAGE
from google.appengine.api import users, memcache
import uuid

from models.comment import Comment
from models.topic import Topic


class CreateTopicHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=user.email(), time=3600)
        params = {"csrf_token": csrf_token}

        if user:
            return self.render_template('topics/topic_new.html', params=params)
        else:
            message = LOGIN_MESSAGE
            params = {"message": message}
            return self.render_template('topics/topic_new.html', params=params)

    def post(self):

        user = users.get_current_user()
        csrf_token = self.request.get("csrf_token")
        csrf_value = memcache.get(csrf_token)
        if user:
            title = self.request.get('title')
            content = self.request.get('content')
            # csrf_token
            if str(csrf_value) != user.email():
                return self.write("You are hacker")

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
        # current user
        user = users.get_current_user()

        # topic details and topic comments
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == int(topic_id)).order(Comment.created_at).fetch()

        # csrf_token
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=user.email(), time=3600)

        parms = {'topic': topic, 'comments': comments, 'csrf_token': csrf_token}
        return self.render_template('topics/topic_details.html', params=parms)

