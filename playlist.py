from gi.repository import Gtk


COLS = {
        'title': 0,
        'artist': 1,
        'album': 2,
        'location': 3}


class Playlist:
    def __init__(self, store:Gtk.ListStore):
        self.store = store
        self.current = None

    def select(self, it:Gtk.TreeIter):
        path = self.store.get_path(it)
        self.current = Gtk.TreeRowReference.new(self.store, path)

    def next(self):
        if self.current is not None and self.current.valid():
            path = self.current.get_path()
            it = self.store.get_iter(path)
            it = self.store.iter_next(it)
            if it is not None:
                self.select(it)
                title = self.store.get_value(it, 0)
                location = self.store.get_value(it, 3)
                return {'title': title, 'location': location}
            else:
                self.current = None
                return None

    def prev(self):
        if self.current is not None and self.current.valid():
            path = self.current.get_path()
            it = self.store.get_iter(path)
            it = self.store.iter_previous(it)
            if it is not None:
                self.select(it)
            else:
                self.current = None
