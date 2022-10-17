from gi.repository import WebKit2, GObject, JavaScriptCore, GLib


class CustomWebView(WebKit2.WebView):

    def __init__(self, on_data_received, on_load_changed=None):
        super(WebKit2.WebView, self).__init__()
        self.on_data_received = on_data_received
        if on_load_changed:
            self.on_load_changed = on_load_changed
        else:
            self.on_load_changed = lambda: 1 + 1

        settings: WebKit2.Settings = self.get_settings()  # type: ignore # type: WebKit2.Settings


        # Python <--> WebView communication
        self.connect('notify::title', self.on_title_change)
        # self.connect('context-menu', self.on_context_menu)
        self.connect('load-changed', self._on_load_changed)

        # Tastatur Navigation
        settings: WebKit2.Settings = self.get_settings()  # type: ignore
        settings.set_enable_spatial_navigation(True)
        settings.set_enable_caret_browsing(True)

    def run_js(self, function):
        '''
        Lässt function auf der Seite laufen, unabhängig von welchem Thread diese Funktion aufgerufen wurde
        '''
        GLib.idle_add(self._run_js, function)

    def _run_js(self):
        self.run_javascript(function)
        return GLib.SOURCE_REMOVE

    # Gebe True zurück, um das Kontext-Menü auszuschalten
    # def on_context_menu(self):
    #     pass

    def on_title_change(self, view, frame):
        '''
        Callback wird benutzt um Daten von JavaScript zu Python zu schicken
        '''
        title = self.get_title()
        if title not in ["null", "", None]:
            self.on_data_received(title)
            self.run_js('document.title = ""')

    def send_data(self, function, data):
        '''
        Kommunikation von Python zu JavaScript

        :param function: Name der Funktion, welche ausgeführt werden soll
        :param data: String mit Daten
        '''
        self.run_js("{0}({1})".format(function, str(data)))


    def _on_load_changed(self, browser=None, web_view: WebKit2.WebView | None = None):
        if not self.is_loading():
            self.on_load_changed()