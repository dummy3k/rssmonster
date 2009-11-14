from rssmonster.tests import *
from rssmonster.lib.reporter import Reporter
from mock import Mock 
from datetime import datetime, timedelta

import logging
log = logging.getLogger(__name__)

def create_mock(values):
    retval = Mock()
    for k in values:
        retval.__dict__[k] = values[k]
        
    return retval
    
class TestReporter(TestController):
    def __init__(self, foo):
        TestController.__init__(self, foo)
        
        log.debug("--- running %s" % foo)
        
    def test_create_mock(self):
        foo = create_mock({'foo':'bar', 'test':'Hello World'})
        self.assertEqual('bar', foo.foo)
        self.assertEqual('Hello World', foo.test)
        
        
    def test_add_ham(self):
        f = Mock()
        r = Reporter(f, datetime(2009,11,14, 12,00), timedelta(minutes=5))

        r.add_item(Mock(), False)
        self.assertTrue(f.add_item.called)
        
        #~ r.add_item(title="Sample post",
                   #~ link="", description="",
                   #~ is_spam=False,
                   #~ pubdate=datetime(2009,11,14, 12,00))
        #~ f.add_item.assert_called_with(title="Sample post",
                   #~ link="", description="",
                   #~ pubdate=datetime(2009,11,14, 12,00))
        #~ 
        #~ f.reset_mock()
        #~ self.assertFalse(f.add_item.called)

    def test_suppress(self):
        #~ user = Mock()
        #~ user.id = 666

        f = Mock()
        r = Reporter(f, datetime(2009,11,14, 12,00), timedelta(minutes=5))

        entry = create_mock({'updated':datetime(2009,11,14, 12,01)})
        r.add_item(entry, True)

        self.assertFalse(f.add_item.called)
        self.assertEqual(entry, r.spam_entries[0])
        self.assertNotEqual(Mock(), r.spam_entries[0])
        self.assertEqual(1, len(r.spam_entries))
