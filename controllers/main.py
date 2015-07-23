from gi.repository import Gtk
from player import Player
from os.path import basename
from models import media

COLS = {
        'title': 0,
        'artist': 1,
        'album': 2,
        'location': 3}

def getMetadata(location):
    try:
        file = media.File.get(media.File.uri==location)
        return dict(file.metadata())
    except:
        return None


class MainCtrl:
    def __init__(self, playlist):
        self.mediaPlayer = Player()
        self.playlist = playlist

    def playSelected(self, tree, path, column):
        model = tree.get_model()
        it = model.get_iter(path)
        self.playlist.select(it)
        location = model.get_value(it, COLS['location'])
        self.mediaPlayer.set_mrl(location)
        self.mediaPlayer.play()

    def play(self, *args):
        self.mediaPlayer.play()

    def pause(self, *args):
        self.mediaPlayer.pause()

    @staticmethod
    def addFiles(store):
        d = Gtk.FileChooserDialog(
            'Add media',
            None,
            Gtk.FileChooserAction.OPEN)
        d.add_button('Accept', Gtk.ResponseType.OK)
        d.add_button('Cancel', Gtk.ResponseType.CANCEL)
        d.set_select_multiple(True)
        res = d.run()

        if res == Gtk.ResponseType.OK:
            for f in d.get_filenames():
                it = store.append()
                store.set_value(it, COLS['location'], f)
                metadata = getMetadata(f)
                if metadata is not None and 'title' in metadata:
                    store.set_value(it, COLS['title'], metadata['title'])
                else:
                    store.set_value(it, COLS['title'], basename(f))

        d.destroy()

    def removeFromPlaylist(self, selection):
        model, paths = selection.get_selected_rows()
        refs = [Gtk.TreeRowReference.new(model, p) for p in paths]
        for ref in refs:
            it = model.get_iter(ref.get_path())
            model.remove(it)

    @staticmethod
    def clearPlaylist(store):
        store.clear()

    @staticmethod
    def quit(*args):
        Gtk.main_quit()
