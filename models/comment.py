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
    def create(cls, content, author,  topic):
        comment = cls(content=content, author_email=author.email(), topic_id=topic.key.id(), topic_title=topic.title)
        comment.put()

        taskqueue.add(url="/task/email-new-comment", params={"topic_author_email": topic.author_email,
                                                             "topic_title": topic.title,
                                                             "comment_content": comment.content})
        return comment

