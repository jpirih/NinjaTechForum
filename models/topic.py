from google.appengine.ext import ndb


class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def crate(cls, content, title, author):
        topic = cls(title=title, content=content, author_email=author.email)
        topic.put()
        return topic

    @classmethod
    def delete(cls, topic):
        topic.deleted = True
        topic.put()
        return topic

    @classmethod
    def reload(cls, topic):
        topic.deleted = False
        topic.put()
        return topic

    @classmethod
    def destroy(cls, topic):
        return topic.key.delete()


