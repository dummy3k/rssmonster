#from Queue import Queue
import logging
log = logging.getLogger(__name__)

class HamEntry():
    def __init__(self, entry):
        self.type = 'ham'
        self.entry = entry
        self.offset_id = entry.id

class SpamEntry():
    def __init__(self):
        self.type = 'spam'
        self.entries = []
        self.offset_id = None

    def add(self, entry):
        self.offset_id = entry.id
        self.entries.append(entry)

def last(array):
    return array[len(array)-1]

class RingBuffer():
    def __init__(self, max):
        self.max = max
        self.buffer = []

    def push(self, item):
        self.buffer.append(item)
        if len(self.buffer) > self.max:
            self.buffer = self.buffer[1:] #pop

    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, index):
        return self.buffer[index]

class Reporter():
    def __init__(self, feed, last_report, last_last_report, delta, add_ham,
                report_spam, max_entries = 30):

        self.feed = feed
        self.delta = delta
        self.last_report = last_report
        self.last_last_report = last_last_report
        self.spam_entries = []
        self.add_ham = add_ham
        self.report_spam = report_spam
        #self.offset_id = None
        self.entry_queue = RingBuffer(max_entries)
        self.offset_queue = RingBuffer(max_entries)
        self.max_entries = max_entries

    def add_item_bak(self, title, link, description, is_spam,
                 author_email=None, author_name=None, author_link=None,
                 pubdate=None, comments=None, unique_id=None,
                 enclosure=None, categories=(), item_copyright=None,
                 ttl=None):
        pass


    def offset_id(self):
        if len(self.spam_entries) > 0:
            return self.spam_entries[0].id

        retval = None
        for e in self.offset_queue.buffer:
            if not retval or retval > e.id:
                retval = e.id
        return retval

    def add_item(self, entry, is_spam):

        if len(self.offset_queue.buffer) == 0:
            self.offset_queue.push(entry)

        if not self.last_report:
            self.last_report = entry.updated

        if entry.updated > self.last_report + self.delta:
            self.report_spam()
            self.last_last_report = self.last_report
            self.last_report = entry.updated
            self.offset_queue.push(self.spam_entries[0])

            spe = SpamEntry()
            spe.entries = self.spam_entries
            self.entry_queue.push(spe)
            self.spam_entries = []

        if not is_spam:
            self.add_ham()

            self.offset_queue.push(entry)
            self.entry_queue.push(HamEntry(entry))
            return

        if entry.updated < self.last_report + self.delta:
            self.spam_entries.append(entry)
            return

