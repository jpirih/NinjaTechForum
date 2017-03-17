from handlers.base import BaseHandler
from helpers.sending_mails import new_comment_emil


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")

        email = new_comment_emil(recipient=topic_author_email, topic_title=topic_title.encode("utf-8"), topic_id=topic_id)
        return email

