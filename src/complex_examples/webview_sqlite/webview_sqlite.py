from gi.repository import Gtk, GLib
import os

from src.complex_examples.webview_sqlite.webview import CustomWebView

'''
NICHT FERTIG!
'''

class WebviewSqlite(Gtk.ApplicationWindow):

    base_folder = os.path.join(os.getcwd(), 'src', 'complex_examples', 'webview_sqlite')
    webview: CustomWebView


    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('Webkit with SQLite')
        self.set_default_size(800, 800)
        self.add(self.get_body())
        self.show_all()

    def get_body(self):
        self.webview = CustomWebView(self.on_data_received)
        self.webview.load_uri(GLib.filename_to_uri(os.path.join(self.base_folder, 'index.html')))
        return self.webview

    def on_data_received(self, data):
        print(data)

    
    def search_in_db(self, search):
        pass

    def _get_db_con(self):
        self._db_connection = 'TODO'

    @property
    def _con(self):
        if not hasattr(self, "_db_connection"):
            self._get_db_con()
        return self._db_connection
