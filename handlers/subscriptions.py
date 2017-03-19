from handlers.base import BaseHandler
from models.subscription import Subscription
from helpers.messages import SUBSCRIBTION_EXIST, SUBSCRIBTION_NEW



class SubscribeToNewTopics(BaseHandler):
    def post(self):
        """ new subscription for latest topics """
        mail = self.request.get('email')
        subscriber = Subscription.query(Subscription.email == mail)
        if not subscriber:
            Subscription.create(email=mail)
            return self.render_template("error.html", params={"message": SUBSCRIBTION_NEW} )
        else:
            return self.render_template("error.html", params={"message": SUBSCRIBTION_EXIST})
