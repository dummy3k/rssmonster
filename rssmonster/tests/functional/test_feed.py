from rssmonster.tests import *

class TestFeedController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='feed', action='index'))
        # Test response...

    def test_show_list(self):
        response = self.app.get(url(controller='feed', action='show_list'))
        # Test response...
