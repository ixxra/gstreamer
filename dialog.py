from gi.repository import Gtk

d = Gtk.FileChooserDialog()
d.add_buttons('Accept', Gtk.ResponseType.OK, 'Cancel', Gtk.ResponseType.CANCEL)
d.set_select_multiple(True)

res = d.run()
print(res)
