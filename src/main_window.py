from gi.repository import Gtk, Gio
from src.complex_examples.webview_sqlite.webview_sqlite import WebviewSqlite

from src.simple_examples.dialog import ExampleDialog
from src.simple_examples.webkit_window import WebKitWindow

'''
Das Hauptfenster des Programms, mit welchem die einzelnen Funktionen
gestartet werden können
'''

class MainWindow(Gtk.ApplicationWindow):
    
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('Hauptfenster')
        self.set_default_size(500, 500)
        # Fügt die Rückgabe von build in das Fenster ein
        self.add(self.build())
        # Nötig um das Fenster zu sehen
        self.show_all()
    
    def build(self):
        # Ein Widget um Elemente in einem Raster anzuordnen https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtkgrid.html
        grid = Gtk.Grid()
        
        # Button: https://athenajc.gitbooks.io/python-gtk-3-api/content/gtk-group/gtkbutton.html
        show_notification_button = Gtk.Button(label='Show Notification')
        # Verbinden des Signals clicked mit der Funktion show_example_notification -> Knopf wird gedrückt, Funktion wird ausgeführt
        show_notification_button.connect('clicked', self.show_example_notification)

        to_webkitWindow_button = Gtk.Button(label='Show WebkitExample')
        to_webkitWindow_button.connect('clicked', self.to_webkitWindow)

        show_dialog_button = Gtk.Button(label='Show Dialog')
        show_dialog_button.connect('clicked', self.show_dialog)

        to_webkit_sqlite_button = Gtk.Button(label='Webkit with Sqlite')
        to_webkit_sqlite_button.connect('clicked', self.to_webkit_sqlite)

        '''
        Die Knöpfe werden in das Raster eingefügt. Mit add an die nächste Position und mit
        grid.attach(Position oben links (x-Achse), Position oben links (y-Achse), Breite, Höhe) an eine
        bestimmte Position gesetzt werden
        '''
        # grid.attach(show_notification_button, 0, 0, 1, 1)
        grid.add(show_notification_button)
        grid.add(to_webkitWindow_button)
        grid.add(show_dialog_button)
        grid.add(to_webkit_sqlite_button)

        return grid


    def show_dialog(self, _):
        dialog = ExampleDialog(self)
        # Zeigt Dialog, blockiert bis Antwort ausgewählt wurde
        response = dialog.run()

        # Verarbeiten der Antwort
        if response == Gtk.ResponseType.OK:
            print("Ok button wurde gedrückt")
        elif response == Gtk.ResponseType.CANCEL:
            print('Cancel button wurde gedrückt')

        # Entfernt Dialog wieder
        dialog.destroy()

    
    def to_webkitWindow(self, _):
        # Erstelle das WebKit Fenster
        webkit_window = WebKitWindow(self.get_application())
        # Zeige das Webkit Fenster
        webkit_window.present()


    def to_webkit_sqlite(self, _):
        webkit_sqlite_window = WebviewSqlite(self.get_application())
        webkit_sqlite_window.present()

    

    def show_example_notification(self, _):
        # Erstelle neue Benachrichtigung
        notification = Gio.Notification()
        notification.set_title('Test Benachrichtigung')
        notification.set_body('Test Benachrichtigungstext')
        notification.set_icon(Gio.ThemedIcon(name='dialog-information-symbolic'))  # type: ignore

        # Standard Aktion, welche ausgeführt wird, wenn auf die Benachrichtigung geklickt wird
        notification.set_default_action('app.notificationAction("beispielParameter")')

        # Buttons für die Benachrichtigung
        notification.add_button('Button Text', 'app.buttonAction("beispielParameter")')

        # Wird nicht angezeigt, da das Programm eine .desktop Datei mit gleicher Programm-Id braucht
        self.get_application().send_notification('beispielBenachrichtigung', notification)  # type: ignore

        self.get_application().withdraw_notification('beispielBenachrichtigung')  # type: ignore


