from libs import sendgrid
from libs.secret import SENDGRID_API_KEY
from libs.sendgrid.helpers.mail import *


def new_comment_emil(recipient, topic_title, topic_id):
    # using SendGrid's Python Library - https://github.com/sendgrid/sendgrid-python

    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email("janko.pirih@gmail.com")
    subject = "New Comment on Topic - {}".format(topic_title)
    to_email = Email(recipient)
    content = Content("text/plain", """You have new comment on topic -  <a href="http://emerald-eon-159115.appspot.com/topic/{1}">{0}</a>""".format(topic_title, topic_id))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

