from gi.repository import Gtk, Gio

class ExampleDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Beispiel Dialog', transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label('Die ist ein Beispieldialog')

        box: Gtk.Box = self.get_content_area()  # type: ignore
        box.add(label)
        self.show_all()
