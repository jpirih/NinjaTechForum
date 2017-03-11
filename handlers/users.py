from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic
from models.user import User
from helpers.tools import OWNER_MESSAGE
from helpers.decorators import validate_csrf
from google.appengine.api import users


class UserLoginHandler(BaseHandler):
    def get(self):
        """ user login  handler """
        current_ueser = users.get_current_user()
        user = User.query(User.email == current_ueser.email()).get()
        if user and user.activated:
            return self.redirect_to('main-page')
        else:
            return self.render_template_with_csrf('users/user_registration.html')

    @validate_csrf
    def post(self):
        """ user first time login save to datastore """
        current_user = users.get_current_user()
        user = User.query(User.email == current_user.email()).get()

        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        birth_date = self.request.get('birth_date')

        user.first_name = first_name
        user.last_name = last_name
        user.birth_date = birth_date
        user.activated = True
        user.put()

        return self.redirect_to('main-page')


class UserProfileHandler(BaseHandler):
    def get(self, user_id):
        """ user profile page view """
        current_user = users.get_current_user()
        user = User.get_by_id(int(user_id))
        my_topics = Topic.query(Topic.author_email == user.email)
        my_comments = Comment.query(Comment.author_email == user.email)
        params = {'my_topics': my_topics, 'my_comments': my_comments}

        if current_user.email() == user.email or User.is_admin(current_user):
            return self.render_template('users/user_profile.html', params=params)
        else:
            message = OWNER_MESSAGE
            params = {'message': message}
            return self.render_template("error.html", params=params)

