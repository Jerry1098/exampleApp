from math import floor
from numbers import Number
from gi.repository import Gtk, WebKit2, Gio, JavaScriptCore, GObject

class WebKitWindow(Gtk.ApplicationWindow):

    # WebView welches eine Website oder eine html-Datei anzeigt
    webview: WebKit2.WebView
    # Label (Text) welcher unter dem Webview angezeigt werden wird
    label: Gtk.Label
    # Boolean ob die Website grade lädt
    is_website_loading = False

    '''
    Erstelle neues Fenster (siehe main_window.py)
    '''
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('WebKit Example')
        self.set_default_size(800, 800)
        self.add(self.get_body())
        self.show_all()

    def get_body(self):
        # Erstelle das Webview
        self.webview = WebKit2.WebView()
        website_data_manager: WebKit2.WebsiteDataManager = self.webview.get_website_data_manager()  # type: ignore

        # Setze die Network-Proxy um ins Internet zu kommen
        proxy_settings = WebKit2.NetworkProxySettings.new(default_proxy_uri='http://proxy.genua.de:8000')
        # website_data_manager.set_network_proxy_settings(proxy_mode=WebKit2.NetworkProxyMode.CUSTOM, proxy_settings=proxy_settings)

        settings = WebKit2.Settings()
        # Einstellung um die Webview Konsole in die Standard-Ausgabe zu schreiben
        settings.set_enable_write_console_messages_to_stdout(True)

        self.webview.set_settings(settings=settings)
        # Das Webview soll sich horizontal und vertical möglichst weit ausbreiten (wichtig für z.B. nicht homogene Grids)
        self.webview.set_vexpand(True)
        self.webview.set_hexpand(True)
        # setze die Uri für das Webview
        self.webview.load_uri('https://www.gnome.org/')

        button = Gtk.Button(label='Send Alert')
        button.connect('clicked', self.run_javascript_button_clicked, None)

        self.label = Gtk.Label(label='Startup')  # type: ignore

        # self.webview.connect('notify::title', lambda x, y: self.label.set_label(self.webview.get_title()))
        self.webview.connect('notify::estimated-load-progress', self.loading_callback)

        grid = Gtk.Grid()
        # alle y-Achsen sind gleich groß
        grid.set_column_homogeneous(True)
        grid.attach(self.webview, 0, 0, 2, 1)
        grid.attach(button, 0, 1, 1, 1)
        grid.attach(self.label, 1, 1, 1, 1)

        return grid
    

    def loading_callback(self, x, y, z=None):
        progress = float(self.webview.get_estimated_load_progress())  # type: ignore
        if progress < 1.0:
            self.label.set_label(f'Loading... \t{floor(progress*100.0)}%')
        else:
            self.label.set_label(self.webview.get_title())

    '''
    Callback Funktion, welche Javascript im Webview ausführt
    '''
    def run_javascript_button_clicked(self, button: Gtk.Button, y: None, callback=None):
        javascript= 'function send_alert() {alert("Alert from Gtk"); return "Success"} send_alert()'
        self.webview.run_javascript(javascript, None, self.button_javascript_callback)

    '''
    Callback Funktion, welche aufgerufen wird, wenn Javascript fertig ausgeführt wurde mit der letzten
    Rückgabe (hier Success von run_javascript_button_clicked())
    '''
    def button_javascript_callback(self, webview: WebKit2.WebView, task: Gio.Task):
        result: WebKit2.JavascriptResult = webview.run_javascript_finish(task)  # type: ignore
        js_value: JavaScriptCore.Value = result.get_js_value()  # type: ignore
        print(js_value.to_string())
