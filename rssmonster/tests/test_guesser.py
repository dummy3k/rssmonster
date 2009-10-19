from rssmonster.tests import *
from rssmonster.lib.guesser import Guesser
from mock import Mock 

import logging
log = logging.getLogger(__name__)

class TestGuesser(TestController):
    def __init__(self, foo):
        TestController.__init__(self, foo)
        
        log.debug("ho")
        
    def test(self):
        log.debug("ho")
        user = Mock()
        user.id = 666
        
        feed = Mock()
        feed.id = 666
        
        g = Guesser(feed, user)
        self.assertEqual(10, 10)

