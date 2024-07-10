import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

class PopupWindow(Gtk.Window):
    def __init__(self):#, application):
        Gtk.Window.__init__(self, title="Text Processor Feedback")#, application=application)
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.move(screen_width - 410, screen_height - 250)

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
        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_key_press)

    def update_content(self, action, result):
        self.action_label.set_text(action)
        self.result_buffer.set_text(result)
        self.show_all()
        self.present()  # This will bring the window to the foreground and give it focus

    def on_delete_event(self, widget, event):
        self.destroy()  # Actually destroy the window instead of hiding
        return False

    def on_focus_out(self, widget, event):
        self.destroy()  # Actually destroy the window instead of hiding
        return False

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()  # Actually destroy the window instead of hiding
            return True
        return False

# class MyApplication(Gtk.Application):
#     def __init__(self):
#         super().__init__(application_id="com.example.TextProcessor",
#                          flags=Gio.ApplicationFlags.FLAGS_NONE)
        
#     def do_activate(self):
#         win = PopupWindow(self)
#         win.update_content("Action", "Result")  # You can customize this as needed
#         win.show_all()
#         win.present()

# def main():
#     app = MyApplication()
#     app.run(None)

# if __name__ == "__main__":
#     main()