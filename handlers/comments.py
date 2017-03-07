from handlers.base import BaseHandler
from google.appengine.api import users, memcache
from helpers.tools import LOGIN_MESSAGE
from models.comment import Comment
from models.topic import Topic


class CreateCommentHandler(BaseHandler):
    def post(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))
        if not user:
            message = LOGIN_MESSAGE
            params = {'message': message}
            return self.render_template('error.html', params=params)

        csrf_token = self.request.get('csrf_token')
        csrf_value = memcache.get(csrf_token)

        if not csrf_value or str(csrf_value) != user.email():
            return self.write('You are hacker')

        content = self.request.get('content')
        new_comment = Comment(content=content, author_email=user.email(), topic_id=int(topic_id), topic_title=topic.title)
        new_comment.put()
        return self.redirect_to('topic-details', topic_id=int(topic_id))



