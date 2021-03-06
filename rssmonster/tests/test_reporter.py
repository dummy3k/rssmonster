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
        self.reporter = Reporter(datetime(2009,11,14, 12,00), None, timedelta(minutes=5))

    def test_suppress(self):
        entry = create_mock({'updated':datetime(2009,11,14, 12,01)})
        self.reporter.add_item(entry, True)

        self.assertEqual(entry, self.reporter.spam_entries[0])
        self.assertNotEqual(Mock(), self.reporter.spam_entries[0])
        self.assertEqual(1, len(self.reporter.spam_entries))

    def test_report_spam(self):
        entry = create_mock({'updated':datetime(2009,11,14, 12,01)})
        self.reporter.add_item(entry, True)
        self.assertEqual(entry, self.reporter.spam_entries[0])

        entry = create_mock({'updated':datetime(2009,11,14, 12,07)})
        self.reporter.add_item(entry, False)
        self.assertEqual(datetime(2009,11,14, 12,07),
            self.reporter.last_report)

class TestReporterInitial(TestController):

    def test_reality(self):
        self.reporter = Reporter(None, None, timedelta(minutes=5))

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,01)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,02)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,03)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,04)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,11)}), True)
        #   report
        self.assertEqual(datetime(2009,11,14, 12,11),
            self.reporter.last_report)
        self.assertEqual(datetime(2009,11,14, 12,01),
            self.reporter.last_last_report)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,22)}), False)
        #   report
        self.assertEqual(datetime(2009,11,14, 12,22),
            self.reporter.last_report)
        self.assertEqual(datetime(2009,11,14, 12,11),
            self.reporter.last_last_report)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,33)}), True)
        #   report
        self.assertEqual(datetime(2009,11,14, 12,33),
            self.reporter.last_report)
        self.assertEqual(datetime(2009,11,14, 12,22),
            self.reporter.last_last_report)

    def test_reality_from_step2(self):
        self.reporter = Reporter(datetime(2009,11,14, 12,11),
            datetime(2009,11,14, 12,01), timedelta(minutes=5))

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,22)}), False)
        #   report
        self.assertEqual(datetime(2009,11,14, 12,22),
            self.reporter.last_report)
        self.assertEqual(datetime(2009,11,14, 12,11),
            self.reporter.last_last_report)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,13)}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,33)}), True)
        #   report
        self.assertEqual(datetime(2009,11,14, 12,33),
            self.reporter.last_report)
        self.assertEqual(datetime(2009,11,14, 12,22),
            self.reporter.last_last_report)


class TestReporterQueued(TestController):
    def setUp(self):
        self.reporter = Reporter(None, None, timedelta(minutes=10), max_entries=5)

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
        self.assertEqual(0, len(self.reporter.entry_queue))
        self.assertEqual(1, self.reporter.spam_entries[0].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,02), 'id':2}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(1, len(self.reporter.entry_queue))
        self.assertEqual('ham', self.reporter.entry_queue[0]['type'])
        self.assertEqual(2, self.reporter.entry_queue[0]['entry'].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,03), 'id':3}), True)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(1, len(self.reporter.entry_queue))
        self.assertEqual(1, self.reporter.spam_entries[0].id)
        self.assertEqual(3, self.reporter.spam_entries[1].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,4), 'id':4}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(2, len(self.reporter.entry_queue))
        self.assertEqual('ham', self.reporter.entry_queue[1]['type'])
        self.assertEqual(2, self.reporter.entry_queue[0]['entry'].id)
        self.assertEqual(4, self.reporter.entry_queue[1]['entry'].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,5), 'id':5}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(2, self.reporter.entry_queue[0]['entry'].id)
        self.assertEqual(4, self.reporter.entry_queue[1]['entry'].id)
        self.assertEqual(5, self.reporter.entry_queue[2]['entry'].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,6), 'id':6}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(2, self.reporter.entry_queue[0]['entry'].id)
        self.assertEqual(4, self.reporter.entry_queue[1]['entry'].id)
        self.assertEqual(5, self.reporter.entry_queue[2]['entry'].id)
        self.assertEqual(6, self.reporter.entry_queue[3]['entry'].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,7), 'id':7}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(2, self.reporter.entry_queue[0]['entry'].id)
        self.assertEqual(4, self.reporter.entry_queue[1]['entry'].id)
        self.assertEqual(5, self.reporter.entry_queue[2]['entry'].id)
        self.assertEqual(6, self.reporter.entry_queue[3]['entry'].id)
        self.assertEqual(7, self.reporter.entry_queue[4]['entry'].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,8), 'id':8}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(4, self.reporter.entry_queue[0]['entry'].id)
        self.assertEqual(5, self.reporter.entry_queue[1]['entry'].id)
        self.assertEqual(6, self.reporter.entry_queue[2]['entry'].id)
        self.assertEqual(7, self.reporter.entry_queue[3]['entry'].id)
        self.assertEqual(8, self.reporter.entry_queue[4]['entry'].id)


        self.assertEqual(datetime(2009,11,14, 12,01),
            self.reporter.last_report)

        #next will trigger report
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':9}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual(6, self.reporter.entry_queue[0]['entry'].id)
        self.assertEqual(7, self.reporter.entry_queue[1]['entry'].id)
        self.assertEqual(8, self.reporter.entry_queue[2]['entry'].id)
        self.assertEqual('spam', self.reporter.entry_queue[3]['type'])
        self.assertEqual(1, self.reporter.entry_queue[3]['entries'][0].id)
        self.assertEqual(3, self.reporter.entry_queue[3]['entries'][1].id)
        self.assertEqual(9, self.reporter.entry_queue[4]['entry'].id)

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,8), 'id':10}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual('spam', self.reporter.entry_queue[2]['type'])

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,8), 'id':11}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual('spam', self.reporter.entry_queue[1]['type'])

        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,8), 'id':12}), False)
        self.assertEqual(1, self.reporter.offset_id())
        self.assertEqual('spam', self.reporter.entry_queue[0]['type'])

        # this popped the spam report entries offset is > 1
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,8), 'id':13}), False)
        self.assertEqual('ham', self.reporter.entry_queue[1]['type'])
        self.assertEqual(9, self.reporter.entry_queue[0]['entry'].id)
        log.debug("offset_queue: %s" % self.reporter.offset_queue[0].id)
        self.assertEqual(9, self.reporter.offset_id())


    def test_spam_only(self):
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,11), 'id':10}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,12), 'id':11}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,22), 'id':20}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,33), 'id':30}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,44), 'id':40}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 12,55), 'id':50}), True)
        self.reporter.add_item(create_mock({'updated':datetime(2009,11,14, 13,06), 'id':60}), True)

        self.assertEqual(10, self.reporter.entry_queue[0]['entries'][0].id)
        self.assertEqual(11, self.reporter.entry_queue[0]['entries'][1].id)
        self.assertEqual(20, self.reporter.entry_queue[1]['entries'][0].id)
        self.assertEqual(30, self.reporter.entry_queue[2]['entries'][0].id)
        self.assertEqual(40, self.reporter.entry_queue[3]['entries'][0].id)
        self.assertEqual(50, self.reporter.entry_queue[4]['entries'][0].id)
