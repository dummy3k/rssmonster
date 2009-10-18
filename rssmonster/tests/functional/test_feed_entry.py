from rssmonster.tests import *

class TestFeedEntryController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='feed_entry', action='index'))
        # Test response...
