from tests.helpers import BaseTest


class MainPageTests(BaseTest):


    def test_main_page_handler(self):
        get = self.testapp.get('/')  # get main handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code
