from gi.repository import Gtk
from gi.repository import Gst
from os.path import basename
from playlist import Playlist
from player import Player
from controllers.timeBar import TimeBarCtrl

COLS = {
        'title': 0,
        'artist': 1,
        'album': 2,
        'location': 3}


class Controller:
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
                store.set_value(it, COLS['title'], basename(f))
                store.set_value(it, COLS['location'], f)

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


class Application:
    def __init__(self):
        b = Gtk.Builder.new_from_file('app.glade')
        store = b.get_object('liststore1')
        playlist = Playlist(store)
        ctrl = Controller(playlist)
        b.connect_signals(ctrl)
        durationLabel = b.get_object('totalDuration')
        positionScale = b.get_object('position')
        timeLabel = b.get_object('currentTime')
        TimeBarCtrl(ctrl.mediaPlayer.pb, timeLabel, positionScale, durationLabel)
        self.playlist = playlist
        self.mainWindow = b.get_object('applicationwindow1')
        self.mediaPlayer = ctrl.mediaPlayer
        self._attachGstEvents(ctrl.mediaPlayer)

    def _attachGstEvents(self, mediaPlayer):
        mediaPlayer.event_attach('message::eos', self.onEos)

    def onEos(self, *args):
        item = self.playlist.next()
        if item is not None:
            self.mediaPlayer.set_mrl(item['location'])
            self.mediaPlayer.play()
        else:
            print('playlist ended')
        return True

    def onMediaPlayerPaused(self, event):
        self.mainWindow.set_title('== Paused ==')
        print('paused', event)

    def onMediaPlayerPlaying(self, event):
        print('playing', self, event)


Gst.init(None)
Gtk.init(None)
app = Application()
app.mainWindow.resize(600,400)
app.mainWindow.show()

Gtk.main()
