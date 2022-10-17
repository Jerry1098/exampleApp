from math import floor
from numbers import Number
from gi.repository import Gtk, WebKit2, Gio, JavaScriptCore, GObject

class WebKitWindow(Gtk.ApplicationWindow):

    webview: WebKit2.WebView
    label: Gtk.Label
    is_website_loading = False

    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('WebKit Example')
        self.set_default_size(800, 800)
        self.add(self.get_body())
        self.show_all()

    def get_body(self):
        self.webview = WebKit2.WebView()
        website_data_manager: WebKit2.WebsiteDataManager = self.webview.get_website_data_manager()  # type: ignore

        proxy_settings = WebKit2.NetworkProxySettings.new(default_proxy_uri='http://proxy.genua.de:8000')
        # website_data_manager.set_network_proxy_settings(proxy_mode=WebKit2.NetworkProxyMode.CUSTOM, proxy_settings=proxy_settings)

        settings = WebKit2.Settings()
        settings.set_enable_write_console_messages_to_stdout(True)

        self.webview.set_settings(settings=settings)
        self.webview.set_vexpand(True)
        self.webview.set_hexpand(True)
        self.webview.load_uri('https://www.gnome.org/')

        button = Gtk.Button(label='Send Alert')
        button.connect('clicked', self.run_javascript_button_clicked, None)

        self.label = Gtk.Label(label='Startup')  # type: ignore

        # self.webview.connect('notify::title', lambda x, y: self.label.set_label(self.webview.get_title()))
        self.webview.connect('notify::estimated-load-progress', self.loading_callback)

        grid = Gtk.Grid()
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

    def run_javascript_button_clicked(self, button: Gtk.Button, y: None, callback=None):
        javascript= 'function send_alert() {alert("Alert from Gtk"); return "Success"} send_alert()'
        self.webview.run_javascript(javascript, None, self.button_javascript_callback)

    def button_javascript_callback(self, webview: WebKit2.WebView, task: Gio.Task):
        result: WebKit2.JavascriptResult = webview.run_javascript_finish(task)  # type: ignore
        js_value: JavaScriptCore.Value = result.get_js_value()  # type: ignore
        print(js_value.to_string())
