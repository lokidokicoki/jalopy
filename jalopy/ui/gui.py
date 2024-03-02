# pylint: disable=wrong-import-position
import gi

gi.require_version("Gtk", "3.0")
# pylint: enable=wrong-import-position

from gi.repository import Gtk
from jalopy.entities.entity_manager import EntityManager

from .base_ui import BaseUI


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Jalo.py")

        self.button = Gtk.Button(label="clickty")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("boop %s", widget)


class Gui(BaseUI):
    def __init__(self, entity_manager: EntityManager):
        super().__init__(entity_manager)

    def main(self):
        win = MainWindow()
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
