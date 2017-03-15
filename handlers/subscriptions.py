from handlers.base import BaseHandler
from models.subscription import Subscription


class SubscribeToNewTopics(BaseHandler):
    def post(self):
        """ new subscription for latest topics """
        mail = self.request.get('email')
        subscriber = Subscription.query(Subscription.email == mail)
        if not subscriber:
            Subscription.create(email=mail)
            return self.write("Thank you for your subscription")
        else:
            return self.write("You are already subscribed")
