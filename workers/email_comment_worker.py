from handlers.base import BaseHandler
from google.appengine.api import mail


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        """ new comment email sender worker """
        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        comment_content = self.request.get("comment_content")

        mail.send_mail(sender="janko.pirih@gmail.com",
                       to=topic_author_email,
                       subject="Dobil -a si nov komentar na temo %s" % topic_title  .encode("utf-8"),
                       body="Nov komentar {}".format(comment_content.encode('utf-8')))
