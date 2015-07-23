from gi.repository import Gtk
from gi.repository import Gst
from playlist import Playlist
from player import Player
from controllers.timeBar import TimeBarCtrl
from controllers.main import MainCtrl


class Application:
    def __init__(self):
        b = Gtk.Builder.new_from_file('app.glade')
        store = b.get_object('liststore1')
        playlist = Playlist(store)
        ctrl = MainCtrl(playlist)
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
