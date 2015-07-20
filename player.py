from gi.repository import Gst

class Player:
    def __init__(self):
        self.pb = Gst.ElementFactory.make('playbin')
        bus = self.pb.get_bus()
        bus.add_watch(0, self.msg)

    def play(self, location):
        self.pb.set_state(Gst.State.NULL)
        self.pb.set_property('uri', Gst.filename_to_uri(location))
        self.pb.set_state(Gst.State.PLAYING)

    def msg(self, *args):
        print(args)
