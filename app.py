import sys
from os import path
sys.path.append(path.abspath('../lib'))

import vlc
from gi.repository import Gtk
from gi.repository import Gst
from os.path import basename
from playlist import Playlist
from player import Player

COLS = {
        'title': 0,
        'artist': 1,
        'album': 2,
        'location': 3}


class Controller:
    def __init__(self, playlist):
        #self.mediaPlayer = vlc.libvlc_new(0, None).media_player_new()
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
        print(*args)
        self.mediaPlayer.play()

    def pause(self, *args):
        print(*args)
        self.mediaPlayer.pause()

    @staticmethod
    def addFiles(store):
        d = Gtk.FileChooserDialog()
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
        self.playlist = playlist
        self.mainWindow = b.get_object('applicationwindow1')
        self.mediaPlayer = ctrl.mediaPlayer
        #self._attachVlcEvents(ctrl.mediaPlayer)
        self._attachGstEvents(ctrl.mediaPlayer)

    def show(self):
        self.mainWindow.show()


    def _attachGstEvents(self, mediaPlayer):
        mediaPlayer.event_attach('message::eos', self.onEos)

    def onEos(self, *args):
        print('MESSAGE: EOS', args)
        item = self.playlist.next()
        if item is not None:
            print(item)
            print(self.mediaPlayer)
            #print(type(item['location']))
            loc = self.playlist.store.get_value(item, 3)
            print(loc)
            self.mediaPlayer.set_mrl(loc)
            #self.mediaPlayer.set_mrl(item['location'])
            self.mediaPlayer.play()
        else:
            print('playlist end', self, event)
        return True

    def onTag(self):
        print('TAG EVENT')

    def _attachVlcEvents(self, mediaPlayer):
        event_manager = mediaPlayer.event_manager()
        #event_manager.event_attach(
        #    vlc.EventType.MediaPlayerPaused,
        #    self.onMediaPlayerPaused)
        #event_manager.event_attach(
        #    vlc.EventType.MediaPlayerPlaying,
        #    self.onMediaPlayerPlaying)
        event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self.onMediaPlayerEndReached, self)

    def onMediaPlayerPaused(self, event):
        self.mainWindow.set_title('== Paused ==')
        print('paused', event)

    def onMediaPlayerPlaying(self, event):
        print('playing', self, event)

    @staticmethod
    def onMediaPlayerEndReached(event, self):
        item = self.playlist.next()
        if item is not None:
            #print(item)
            #print(self.mediaPlayer)
            #print(type(item['location']))
            loc = self.playlist.store.get_value(item, 3)
            print(loc)
            self.mediaPlayer.set_mrl(loc)
            #self.mediaPlayer.set_mrl(item['location'])
            self.mediaPlayer.play()
        else:
            print('playlist end', self, event)


Gst.init(None)
app = Application()
app.mainWindow.resize(600,400)
app.show()

Gtk.main()
