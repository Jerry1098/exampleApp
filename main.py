import sys
from gi.repository import Gtk, Gio
from main_window import MainWindow
from webkit_window import WebKitWindow



class ExampleApplication(Gtk.Application):
    '''
    Hauptprogramm als Singleton
    '''

    def __init__(self):
        '''
        Einstiegspunkt: zum Überschreiben der Eltern-Klasse und erstellen von Globalen Shortcuts
        '''
        super().__init__(application_id='org.example.exampleProgram', flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action, ['<primary>a'])
        self.create_action('preferences', self.on_preferences_action)
    
    def do_activate(self):
        '''
        Wird aufgerufen, wenn das Programm aktiviert wird.

        Das Hauptfenster wird gezeigt, erstellt wenn es nötig ist
        '''
        win = self.props.active_window  # type: ignore
        if not win:
            win = MainWindow(application=self)
        win.present()
    
    def on_about_action(self, widget, _):
        '''
        Callback für app.about aktion
        '''
        about = Gtk.AboutDialog(
            transient_for=self.props.active_window,  # type: ignore
            modal=True,
            program_name='Beispiel Programm',
            logo_icon_name='org.example.exampleProgram',
            version='0.1.0',
            authors=['Jeremias'],
            copyright='© 2022 Jeremias'
        )
        about.present()

    def on_quit_action(self, widget, _):
        self.quit()

    def on_preferences_action(self, widget, _):
        '''Callback für app.preferences aktion'''
        print('app.preferences action aktiviert')

    def create_action(self, name, callback, shortcuts=None):
        '''
        Füge eine Programm-Aktion hinzu.

        Args:
            name: Name der Aktion
            callback: die Funktion, welche aufgerufen wird, wenn die Aktion aktiviert wird
            shortcuts: eine optionale Liste von Shortcuts
        '''
        action: Gio.SimpleAction = Gio.SimpleAction.new(name, None)  # type: ignore
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)

def main(version):
    '''
    Programm Startpunkt
    '''
    app = ExampleApplication()
    return app.run(sys.argv)


