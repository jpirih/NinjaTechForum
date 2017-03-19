import datetime
from handlers.base import BaseHandler
from models.topic import Topic
from models.subscription import Subscription
from helpers.sending_mails import newest_topics_email


class NewestTopicsCron(BaseHandler):
    def get(self):
        """ list of topics that were updated in last 24 hours """

        # get the topics from datastore
        time_24_hours_old = datetime.datetime.now() - datetime.timedelta(hours=24)
        newest_topics = Topic.query(Topic.updated_at < time_24_hours_old, Topic.deleted == False).fetch()

        # list of topic idents for links
        topics_idents = [topic.key.id() for topic in newest_topics]
        # get all subscribers from datastore
        subscribers = Subscription.query(Subscription.subscribed == True).fetch()
        # list of emails
        emails = [subscriber.email for subscriber in subscribers]

        urls = ""

        # building topics links and sending mails
        if newest_topics:
            for topic_id in topics_idents:
                urls += "<li>http://emerald-eon-159115.appspot.com/topic/{}\n</li>".format(topic_id)

            for email in emails:
                newest_topics_email(email, urls)

