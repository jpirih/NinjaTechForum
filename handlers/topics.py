from handlers.base import BaseHandler
from helpers.tools import LOGIN_MESSAGE
from google.appengine.api import users

from models.topic import Topic


class CreateTopicHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            return self.render_template('topics/topic_new.html')
        else:
            login_message = LOGIN_MESSAGE
            params = {"login_message": login_message}
            return self.render_template('topics/topic_new.html', params=params)

    def post(self):
        user = users.get_current_user()
        if user:
            title = self.request.get('title')
            content = self.request.get('content')

            new_topic = Topic(title=title, content=content, author_email=user.email())
            new_topic.put()
            return self.redirect_to('main-page')
        else:
            login_message = LOGIN_MESSAGE
            return self.write(login_message)


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        parms = {'topic': topic}
        return self.render_template('topics/topic_details.html', params=parms)

