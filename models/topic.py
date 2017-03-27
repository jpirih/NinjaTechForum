from google.appengine.ext import ndb

from models.comment import Comment


class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def crate(cls, content, title, author):
        """ create new topic """
        topic = cls(title=title, content=content, author_email=author.email)
        topic.put()
        return topic

    @classmethod
    def update(cls, topic, new_title, new_content):
        """ update topic details title and description """
        topic.title = new_title
        topic.content = new_content
        topic.put()
        return topic

    @classmethod
    def delete(cls, topic):
        """ topic soft delete """
        topic.deleted = True
        topic.put()
        return topic

    @classmethod
    def reload(cls, topic):
        """ reload topic undo topic soft delete """
        topic.deleted = False
        topic.put()
        return topic

    @classmethod
    def destroy(cls, topic):
        """ delete from datastore completely topic and all related comments """
        comments = Comment.query(Comment.topic_id == topic.key.id()).fetch()
        for comment in comments:
            comment.key.delete()

        return topic.key.delete()


