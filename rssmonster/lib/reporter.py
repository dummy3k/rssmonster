import logging
log = logging.getLogger(__name__)

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
        self.offset_id = None

    def add_item_bak(self, title, link, description, is_spam,
                 author_email=None, author_name=None, author_link=None,
                 pubdate=None, comments=None, unique_id=None,
                 enclosure=None, categories=(), item_copyright=None,
                 ttl=None):
        pass

    def add_item(self, entry, is_spam):
        if not self.last_report:
            self.last_report = entry.updated

        if entry.updated > self.last_report + self.delta:
            self.report_spam()
            self.last_last_report = self.last_report
            self.last_report = entry.updated

        if not is_spam:
            #~ self.feed.add_item(title="title", link="link",
                #~ description="description", pubdate=entry.updated)
            self.add_ham()
            return

        if entry.updated < self.last_report + self.delta:
            self.spam_entries.append(entry)
            return

