from helpers.secret import SENDGRID_API_KEY
from sendgird import sendgrid, python_http_client
from sendgird.helpers import mail


def new_comment_emil(recipient, topic_title, topic_id):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    to_email = mail.Email(recipient)
    from_email = mail.Email("janko.pirih@gmail.com")
    subject = "New comment on your topic {0}".format(topic_title)
    content = mail.Content("Your topic {0} received a new comment.Click <a href='http://your-domain.org/topic/{1}'>on this link</a> to see it".format(topic_title.encode("utf-8"), topic_id))
    message = mail.Mail(from_email=from_email, subject=subject, to_email=to_email, content=content)
    response = sg.client.mail.s.post(request_body=message.get())
    return response
