import os
import datetime
import lnote
from html2text import html2text
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import NoteSortOrder

AUTH_TOKEN = 'dev'
MY_NOTES = '/home/jean-louis/Documents/EverNote/'

def modificationDate(path):
    """
    Returns a date object from a given file
    """
    t = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(t)

def saveToJSON(**kwargs):
    """
    Saves notes into JSON file
    """
    for key, value in kwargs.iteritems():
        if key == 'content':
            print "%s = %s" % (key, html2text(value.decode('utf8')))
        else:
            print "%s = %s" % (key, value)

def main():
    client = EvernoteClient(token=AUTH_TOKEN)
    note_store = client.get_note_store()

    updated_filter = NoteFilter(order=NoteSortOrder.UPDATED)
    offset = 0
    max_notes = 100
    result_spec = NotesMetadataResultSpec(includeTitle=True)
    result_list = note_store.findNotesMetadata(AUTH_TOKEN, updated_filter, offset, max_notes, result_spec)

    lnotes = []

    # note is an instance of NoteMetadata
    # result_list is an instance of NotesMetadataList
    for note in result_list.notes:
        rnote_content = note_store.getNoteContent(AUTH_TOKEN, note.guid)
        local_note = lnote.Note(note.guid, note.title, rnote_content)
        lnotes.append(local_note)

    for note in lnotes:
        saveToJSON(**note.__dict__)

if __name__ == "__main__":
    main()
