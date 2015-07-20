from gi.repository import GLib
from gi.repository import Gst


class TimeBarCtrl:
    def __init__(self, playbin, timeLabel, positionScale, totalDuration):
        self.pb = playbin
        self.timeLabel = timeLabel
        self.scale = positionScale
        self.durationLabel = totalDuration
        self._duration = 0
        self._timeoutId = 0
        self._pressed = False
        self._connectSignals()
        self._reset()

    def _connectSignals(self):
        self.scale.connect('button-press-event', self.onScalePressed)
        self.scale.connect('button-release-event', self.onScaleReleased)
        bus = self.pb.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', self.reset)
        bus.connect('message::duration-changed', self.updateDuration)
        bus.connect('message::state-changed', self.onStateChanged)

    def onScalePressed(self, *args):
        self._pressed = True

    def onScaleReleased(self, *args):
        self._pressed = False
        if self._duration != 0:
            pos = self.scale.get_value() * self._duration * 10**9 / 100
            if self.pb.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, pos):
                self.updatePosition()

    def _reset(self):
        self._duration = 0
        self.timeLabel.set_text('00:00')
        self.scale.set_value(0.0)
        self.durationLabel.set_text('00:00')

    def reset(self, bus, msg):
        self._reset()
        return True

    def onStateChanged(self, bus, msg):
        old_state, new_state, pending_state = msg.parse_state_changed()
        if new_state == Gst.State.NULL and self._timeoutId != 0:
            GLib.source_remove(self._timeoutId)
            self._timeoutId = 0
        elif new_state == Gst.State.PAUSED and self._timeoutId != 0:
            GLib.source_remove(self._timeoutId)
            self._timeoutId = 0
        elif new_state == Gst.State.PLAYING:
            self._timeoutId = GLib.timeout_add_seconds(1, self.updatePosition)
        return True

    def updateDuration(self, bus, msg):
        ok, duration = self.pb.query_duration(Gst.Format.TIME)
        if ok:
            duration = duration / 10**9
            self._duration = duration
            self.durationLabel.set_text(self._formatTime(duration))
        return True

    def updatePosition(self):
        ok, pos = self.pb.query_position(Gst.Format.TIME)
        if ok and self._duration != 0:
            time = pos / 10**9
            pct = time / self._duration * 100
            if not self._pressed:
                self.scale.set_value(pct)
            self.timeLabel.set_text(self._formatTime(time))
        else:
            self.scale.set_value(0.0)
        return True

    def _formatTime(self, secs):
        min = int(secs // 60)
        secs = int(secs % 60)
        return '{0:02}:{1:02}'.format(min, secs)
