import functools as fn
from gi.repository import Gtk
from models import media
from os.path import basename


COL = {
    'key'  : 0,
    'value': 1,
    'fileName' : 2,
    'fileLocation': 3}


class Main(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)
        self._setupUi()

    def _setupUi(self):
        toolbar = Gtk.Toolbar()
        addButton = Gtk.ToolButton()
        addButton.set_icon_name('list-add')
        addButton.set_tooltip_text('Add selection to playlist')
        toolbar.insert(addButton, 0)
        entry = Gtk.SearchEntry()
        entry.set_placeholder_text('Search')
        hbox = Gtk.HBox(False, 0)
        hbox.pack_start(toolbar, False, True, 0)
        hbox.pack_start(entry, True, True, 5)
        view = Gtk.TreeView()
        view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        scroll = Gtk.ScrolledWindow()
        scroll.add(view)
        self.do_make_view_columns(view)
        store = Gtk.ListStore(str, str, str, str)
        view.set_model(store)
        box = Gtk.VBox(False, 0)
        box.pack_start(hbox, False, True, 5)
        box.pack_start(scroll, True, True, 0)
        self.add(box)
        entry.connect('activate', self.search, store)

    def search(self, entry, store):
        from peewee import fn
        text = entry.get_text()
        store.clear()
        Tag = media.Tag
        File = media.File
        q = Tag.select(Tag.file).where(Tag.value.contains(text)).distinct()
        q2 = File.select(File,Tag).join(Tag).where(Tag.file << q).aggregate_rows()
        for file in q2:
            it = store.append()
            uri = file.uri
            store.set_value(it, COL['fileName'], basename(uri))
            store.set_value(it, COL['fileLocation'], uri)
            for tag in file.tags:
                it = store.append()
                store.set_value(it, COL['key'], tag.key)
                store.set_value(it, COL['value'], tag.value)

    def do_make_view_columns(self, view):
        render = Gtk.CellRendererText()
        for t in 'key', 'value', 'fileName':
            col = Gtk.TreeViewColumn()
            col.set_title(t.upper())
            col.pack_start(render, True)
            col.add_attribute(render, 'text', COL[t])
            col.set_expand(True)
            view.append_column(col)


if __name__ == '__main__':
    app = Main()
    app.connect('delete-event', Gtk.main_quit)

    app.resize(500, 500)
    app.show_all()

    Gtk.main()
