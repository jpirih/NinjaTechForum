from libs import sendgrid
from libs.secret import SENDGRID_API_KEY, MY_EMAIL
from libs.sendgrid.helpers.mail import *


def new_comment_emil(recipient, topic_title, topic_id):

    """ Sending mail when new commment on topic to topic author """
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email("janko.pirih@gmail.com")
    subject = "New Comment on Topic - {}".format(topic_title)
    to_email = Email(recipient)
    content = Content("text/html", """You have new comment on topic -  <a href="http://emerald-eon-159115.appspot.com/topic/{1}">{0}</a>""".format(topic_title, topic_id))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    return response


def newest_topics_email(recipient, links):
    """ sending mail list of latest topics to subscribers """
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email("janko.pirih@gmail.com")
    subject = "The latest and gratest topics on NinjaTechForum"
    to_email = Email(recipient)
    content = Content("text/html", links)

    mail = Mail(from_email, subject,to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    return response


