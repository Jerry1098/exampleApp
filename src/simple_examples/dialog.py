from gi.repository import Gtk

'''
Simple Dialog-Klasse mit zwei Antwortmöglichkeiten
'''

class ExampleDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Beispiel Dialog', transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        # https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtklabel.html
        label = Gtk.Label('Die ist ein Beispieldialog')

        # https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtkbox.html
        box: Gtk.Box = self.get_content_area()  # type: ignore
        box.add(label)
        self.show_all()
