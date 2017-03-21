""" helper functions for tests """
from models.topic import Topic
from models.user import User
from google.appengine.api import memcache
import uuid






def create_test_user(first_name="Test", last_name="User", email="some.user@example.com",
                     nickname="test.user", activated=True):

    user = User(first_name=first_name, last_name=last_name, email=email, nickname=nickname, activated=activated)
    return user

def create_test_admin(first_name="Test", last_name="Admin", email="admin.user@example.com",
                 nickname="test.user", activated=True, admin=True):

    admin_user = User(first_name=first_name, last_name=last_name, email=email, nickname=nickname, activated=activated)
    return admin_user



def create_test_csrf_token():
    csrf_token = str(uuid.uuid4())
    user = create_test_admin()
    memcache.add(key=csrf_token, value=user.email, time=600)
    return csrf_token


def create_test_topic(title="New Test Topic", content="This is test.topic", author=None):

    if not author:
        test_author = create_test_admin()
        topic = Topic.crate(title=title, content=content, author=test_author)

    topic = Topic.crate(title=title, content=content, author=author)
    return topic