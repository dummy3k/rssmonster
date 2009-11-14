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

class TestLearningMocking(TestController):
    def test_create_mock(self):
        foo = create_mock({'foo':'bar', 'test':'Hello World'})
        self.assertEqual('bar', foo.foo)
        self.assertEqual('Hello World', foo.test)

class TestReporter(TestController):
    def __init__(self, foo):
        TestController.__init__(self, foo)

        log.debug("--- running %s" % foo)

    def setUp(self):
        self.reporter = Reporter(Mock(), datetime(2009,11,14, 12,00),
            None, timedelta(minutes=5), Mock(), Mock())

    def test_add_ham(self):
        self.reporter.add_item(Mock(), False)
        self.assertTrue(self.reporter.add_ham.called)

        #~ self.reporter.add_item(title="Sample post",
                   #~ link="", description="",
                   #~ is_spam=False,
                   #~ pubdate=datetime(2009,11,14, 12,00))
        #~ f.add_item.assert_called_with(title="Sample post",
                   #~ link="", description="",
                   #~ pubdate=datetime(2009,11,14, 12,00))
        #~
        #~ f.reset_mock()
        #~ self.assertFalse(self.reporter.add_ham.called)

    def test_suppress(self):
        entry = create_mock({'updated':datetime(2009,11,14, 12,01)})
        self.reporter.add_item(entry, True)

        self.assertFalse(self.reporter.add_ham.called)
        self.assertEqual(entry, self.reporter.spam_entries[0])
        self.assertNotEqual(Mock(), self.reporter.spam_entries[0])
        self.assertEqual(1, len(self.reporter.spam_entries))

    def test_report_spam(self):
        entry = create_mock({'updated':datetime(2009,11,14, 12,01)})
        self.reporter.add_item(entry, True)
        self.assertFalse(self.reporter.add_ham.called)
        self.assertEqual(entry, self.reporter.spam_entries[0])

        entry = create_mock({'updated':datetime(2009,11,14, 12,07)})
        self.reporter.add_item(entry, False)
        self.assertTrue(self.reporter.add_ham.called)
        self.assertTrue(self.reporter.report_spam.called)
        self.assertEqual(datetime(2009,11,14, 12,07),
            self.reporter.last_report)

class TestReporterInitial(TestController):
    pass

    #~ def test_reality(self):
        #~ self.reporter = Reporter(Mock(), None, None, timedelta(minutes=5), Mock(), Mock())
        #~ #self.assertEqual(None, self.reporter.last_last_report)
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,01)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,02)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,03)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,04)}), True)
        #~ self.assertFalse(self.reporter.report_spam.called)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,11)}), True)
        #~ #   report
        #~ self.assertTrue(self.reporter.report_spam.called)
        #~ self.assertEqual(datetime(2009,11,14, 12,11),
            #~ self.reporter.last_report)
        #~ self.assertEqual(datetime(2009,11,14, 12,01),
            #~ self.reporter.last_last_report)
#~ #        self.assertEqual(None, self.reporter.last_last_report)
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,22)}), False)
        #~ #   report
        #~ self.assertEqual(datetime(2009,11,14, 12,22),
            #~ self.reporter.last_report)
        #~ self.assertEqual(datetime(2009,11,14, 12,11),
            #~ self.reporter.last_last_report)
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,33)}), True)
        #~ #   report
        #~ self.assertEqual(datetime(2009,11,14, 12,33),
            #~ self.reporter.last_report)
        #~ self.assertEqual(datetime(2009,11,14, 12,22),
            #~ self.reporter.last_last_report)
#~
    #~ def test_reality_from_step2(self):
        #~ self.reporter = Reporter(Mock(), datetime(2009,11,14, 12,11),
            #~ datetime(2009,11,14, 12,01), timedelta(minutes=5), Mock(), Mock())
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,22)}), False)
        #~ #   report
        #~ self.assertEqual(datetime(2009,11,14, 12,22),
            #~ self.reporter.last_report)
        #~ self.assertEqual(datetime(2009,11,14, 12,11),
            #~ self.reporter.last_last_report)
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,33)}), True)
        #~ #   report
        #~ self.assertEqual(datetime(2009,11,14, 12,33),
            #~ self.reporter.last_report)
        #~ self.assertEqual(datetime(2009,11,14, 12,22),
            #~ self.reporter.last_last_report)


class TestReporterQueued(TestController):
    def setUp(self):
        self.reporter = Reporter(Mock(), None, None, timedelta(minutes=10), Mock(), Mock(),
            max_entries=5)

    def test_ham_only(self):
        self.assertEqual(None, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':1}), False)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':2}), False)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':3}), False)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':4}), False)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':5}), False)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':6}), False)
        self.assertEqual(2, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':7}), False)
        self.assertEqual(3, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':8}), False)
        self.assertEqual(4, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':9}), False)
        self.assertEqual(5, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':10}), False)
        self.assertEqual(6, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':11}), False)
        self.assertEqual(7, self.reporter.offset_id())

    def test_with_spam(self):
        self.assertEqual(None, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,01), 'id':1}), True)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,02), 'id':2}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual('ham', self.reporter.entry_queue[0].type)
        self.assertEqual(2, self.reporter.entry_queue[0].entry.id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,03), 'id':3}), True)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual('ham', self.reporter.entry_queue[0].type)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,4), 'id':4}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual('ham', self.reporter.entry_queue[0].type)
        self.assertEqual(4, self.reporter.entry_queue[1].entry.id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':5}), False)
        self.assertEqual(1, self.reporter.offset_id())

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':6}), False)
        self.assertEqual(2, self.reporter.offset_id())

        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':7}), False)
        #~ self.assertEqual(3, self.reporter.offset_id())
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':8}), False)
        #~ self.assertEqual(4, self.reporter.offset_id())
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':9}), False)
        #~ self.assertEqual(5, self.reporter.offset_id())
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':10}), False)
        #~ self.assertEqual(6, self.reporter.offset_id())
#~
        #~ self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':11}), False)
        #~ self.assertEqual(7, self.reporter.offset_id())



