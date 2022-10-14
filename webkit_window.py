from gi.repository import Gtk

class WebKitWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('WebKit Example')
        self.set_default_size(800, 800)
        self.add(Gtk.Label('WebKit Example'))
        self.show_all()