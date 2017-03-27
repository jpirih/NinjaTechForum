""" Datastore model for saving  comments """

from google.appengine.ext import ndb
from google.appengine.api import taskqueue


class Comment(ndb.Model):
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, content, user, topic):
        """ create new comment  """
        comment = Comment(content=content, author_email=user.email, topic_id=topic.key.id(), topic_title=topic.title)
        comment.put()

        # run background task to send email to topic author
        # taskqueue.add(url='/task/email-new-comment', params={"topic_author_email": topic.author_email, "topic_title": topic.title, "topic_id": topic.key.id()})

        return comment

    @classmethod
    def update(cls, comment, new_content):
        """ update existing comment """
        comment.content = new_content
        comment.put()
        return comment

    @classmethod
    def delete(cls, comment):
        """ comment soft delete  """
        comment.deleted = True
        comment.put()
        return comment

    @classmethod
    def reload(cls, comment):
        """ Comment reaload - undo comment soft delete """
        comment.deleted = False
        comment.put()
        return comment

    @classmethod
    def destroy(cls, comment):
        return  comment.key.delete()

