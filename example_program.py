import sys
import signal
import locale
import gettext
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")

VERSION = '0.1.0'
pkgdatadir = 'data'
localdir = 'local'

sys.path.insert(1, pkgdatadir)
signal.signal(signal.SIGINT, signal.SIG_DFL)
locale.bindtextdomain('exampleProgram', localdir)
locale.textdomain('exampleProgram')
gettext.install('exampleProgram', localdir)

if __name__ == '__main__':
    # import gi

    # from gi.repository import Gio
    # # Effizienter weg um Ressourcen zu laden und im Programm zu teilen, allerdings müssten diese kompiliert werden
    # resource = Gio.Resource.load(os.path.join(pkgdatadir, 'exampleProgram.gresource'))
    # resource._register()

    from main import main
    sys.exit(main(VERSION))  # type: ignore
