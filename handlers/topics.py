from handlers.base import BaseHandler
from helpers.decorators import validate_csrf, login_required
from helpers.tools import show_info_page
from helpers.messages import TOPIC_AUTHOR


from models.comment import Comment
from models.topic import Topic
from models.user import User


class CreateTopicHandler(BaseHandler):
    @login_required
    def get(self):
        """ create topic form view """
        return self.render_template_with_csrf('topics/topic_new.html')

    @login_required
    @validate_csrf
    def post(self):
        """ save new topic  to datastore """
        user = User.logged_in_user()

        title = self.request.get('title')
        content = self.request.get('content')

        # add new topic
        Topic.crate(title=title, content=content, author=user)

        return self.redirect_to('main-page')


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        """ topic details and topic related comments """
        # current user
        user = User.logged_in_user()
        # selected topic with related comments
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == int(topic_id), Comment.deleted==False).order(Comment.created_at).fetch()

        parms = {'topic': topic, 'comments': comments, 'user': user}
        return self.render_template_with_csrf('topics/topic_details.html', params=parms)


class DeleteTopicHandler(BaseHandler):
    @login_required
    def post(self, topic_id):
        """ topic soft delete hahdler only by author or admin """
        topic = Topic.get_by_id(int(topic_id))
        user = User.logged_in_user()
        if User.is_admin(user) or User.is_author(user, topic):
            Topic.delete(topic)
            return self.redirect_to('main-page')
        else:
            return show_info_page(self, message=TOPIC_AUTHOR)


class ReloadTopic(BaseHandler):
    @login_required
    def post(self, topic_id):
        """ topic reload hahdler only by author or admin """
        topic = Topic.get_by_id(int(topic_id))
        user = User.logged_in_user()
        if User.is_admin(user):
            Topic.reload(topic)
            return self.redirect_to('main-page')
        else:
            return self.write('only admin can reload topic')


class DestroyTopic(BaseHandler):
    @login_required
    def post(self, topic_id):
        """ topic hard delete hahdler only by author or admin """
        topic = Topic.get_by_id(int(topic_id))
        user = User.logged_in_user()
        if User.is_admin(user):
            Topic.destroy(topic)
            return self.redirect_to('main-page')
        else:
            return self.write('only admin can delete topic')


class DeletedTopicsListHandler(BaseHandler):
    @login_required
    def get(self):
        """ list of all deleted topics  to completely delete or renew admin only """
        user = User.logged_in_user()

        if User.is_admin(user):
            topics = Topic.query(Topic.deleted == True).fetch()
            params = {"topics": topics}
            return self.render_template("topics/topics_deleted_list.html", params=params)
        else:
            return self.write("This page can be accessed only by admin")




