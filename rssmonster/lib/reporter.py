#from Queue import Queue
import logging
log = logging.getLogger(__name__)

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
    def __init__(self, last_report, last_last_report, delta, max_entries = 30):

        self.delta = delta
        self.last_report = last_report
        self.last_last_report = last_last_report
        self.spam_entries = []
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
        #~ if len(self.spam_entries) > 0:
            #~ return self.spam_entries[0].id
#~
        #~ retval = None
        #~ for e in self.offset_queue.buffer:
            #~ if not retval or retval > e.id:
                #~ retval = e.id
        #~ return retval
        retval = None
        for e in self.entry_queue:
            if e['type'] == 'ham':
                if not retval or retval > e['entry'].id:
                    retval = e['entry'].id
            elif e['type'] == 'spam':
                for ee in e['entries']:
                    if not retval or retval > ee.id:
                        retval = ee.id

        for ee in self.spam_entries:
            if not retval or retval > ee.id:
                retval = ee.id

        return retval

    def add_item(self, entry, is_spam):

        if len(self.offset_queue.buffer) == 0:
            self.offset_queue.push(entry)

        if not self.last_report:
            self.last_report = entry.updated

        if entry.updated and entry.updated > self.last_report + self.delta and len(self.spam_entries):
            self.last_last_report = self.last_report
            self.last_report = entry.updated
            self.offset_queue.push(self.spam_entries[0])

            self.entry_queue.push({'type':'spam', 'entries':self.spam_entries})
            self.spam_entries = []

        if is_spam:
            self.spam_entries.append(entry)
        else:
            self.offset_queue.push(entry)
            self.entry_queue.push({'type':'ham', 'entry':entry})

