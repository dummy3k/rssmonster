from rssmonster.tests import *

class TestBayesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='bayes', action='index'))
        # Test response...