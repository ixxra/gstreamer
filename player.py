from gi.repository import Gst

class Player:
    def __init__(self):
        self.pb = Gst.ElementFactory.make('playbin')
        self.pb.get_bus().add_signal_watch()

    def play(self):
        self.pb.set_state(Gst.State.PLAYING)

    def set_mrl(self, location):
        self.pb.set_state(Gst.State.NULL)
        self.pb.set_property('uri', Gst.filename_to_uri(location))

    def pause(self):
        self.pb.set_state(Gst.State.PAUSED)

    def msg(self, bus, msg):
        print(msg)
        print(Gst.MessageType.get_name(msg.type))
        return True

    def event_attach(self, name, callback):
        self.pb.get_bus().connect(name, callback)
