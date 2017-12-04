class Note(object):
    """Local wrapper for Evernote note"""
    def __init__(self, guid=None, title=None, content=None):
        self.guid = guid
        self.title = title
        self.content = content
