from gi.repository import Gtk, Gio

from src.simple_examples.dialog import ExampleDialog
from src.simple_examples.webkit_window import WebKitWindow

class MainWindow(Gtk.ApplicationWindow):
    
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('Hauptfenster')
        self.set_default_size(500, 500)
        self.add(self.build())
        self.show_all()
    
    def build(self):
        grid = Gtk.Grid()
        
        show_notification_button = Gtk.Button(label='Show Notification')
        show_notification_button.connect('clicked', self.show_example_notification)

        to_webkitWindow_button = Gtk.Button(label='Show WebkitExample')
        to_webkitWindow_button.connect('clicked', self.to_webkitWindow)

        show_dialog_button = Gtk.Button(label='Show Dialog')
        show_dialog_button.connect('clicked', self.show_dialog)

        # grid.attach(show_notification_button, 0, 0, 1, 1)
        grid.add(show_notification_button)
        grid.add(to_webkitWindow_button)
        grid.add(show_dialog_button)

        return grid


    def show_dialog(self, _):
        dialog = ExampleDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Ok button wurde gedrückt")
        elif response == Gtk.ResponseType.CANCEL:
            print('Cancel button wurde gedrückt')

        dialog.destroy()

    
    def to_webkitWindow(self, _):
        webkit_window = WebKitWindow(self.get_application())
        webkit_window.present()

    

    def show_example_notification(self, _):
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


