from rssmonster.tests import *
from rssmonster.lib.guesser import Guesser, my_tokenize
from mock import Mock 

import logging
log = logging.getLogger(__name__)

class TestGuesser(TestController):
    def test(self):
        user = Mock()
        user.id = 666
        
        feed = Mock()
        feed.id = 666
        
        g = Guesser(feed, user, self.config)
        self.assertEqual(10, 10)

    def test_tokenize(self):
        input = "Augenblick: Leichtigkeit@ des Seins"
        ret = my_tokenize(input, [])
        self.assertTrue('leichtigkeit' in ret)
        self.assertFalse('des' in ret) # less then 4 chars
        self.assertTrue('seins' in ret)
#        self.assertTrue('augenblick' in ret)
        pass
