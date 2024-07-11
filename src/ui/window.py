import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib
import logging

logger = logging.getLogger(__name__)

class PopupWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Text Processor Feedback")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        self.set_position() 

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.action_label = Gtk.Label()
        self.box.pack_start(self.action_label, True, True, 0)

        self.result_view = Gtk.TextView()
        self.result_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.result_buffer = self.result_view.get_buffer()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.result_view)
        self.box.pack_start(scrolled_window, True, True, 0)

        self.connect("delete-event", self.on_delete_event)
        self.connect("key-press-event", self.on_key_press)
    
    def set_position(self):
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.move(screen_width - 410, screen_height - 250)

    def update_content(self, action, result):
        self.action_label.set_text(action)
        self.result_buffer.set_text(result)
        self.set_position()
        self.show_all()

    def on_delete_event(self, widget, event):
        self.hide()
        return True  
    
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.hide()  
        return False