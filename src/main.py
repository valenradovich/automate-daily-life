import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Keybinder', '3.0')
from gi.repository import Gtk, Keybinder, GLib
from dotenv import load_dotenv
import logging
from ui.window import PopupWindow
from services.text_processor import TextProcessor
from utils.clipboard_utils import ClipboardUtils

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextProcessorApp:
    def __init__(self):
        logger.info("Initializing Text Processor App")
        self.feedback_window = PopupWindow()
        self.text_processor = TextProcessor()
        self.clipboard_utils = ClipboardUtils()
        
        # status icon
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_icon_name("accessories-text-editor")
        self.status_icon.set_visible(True)
        self.status_icon.connect("activate", self.on_tray_icon_activate)
        self.status_icon.connect("popup-menu", self.on_tray_icon_popup_menu)


    def run(self):
        logger.info("Running Text Processor App")
        Keybinder.init()
        Keybinder.bind("<Ctrl><Alt>Q", self.translate_text)
        Keybinder.bind("<Ctrl><Alt>G", self.check_text)
        Keybinder.bind("<Ctrl><Alt>S", self.search_text)
        Keybinder.bind("<Ctrl><Alt>A", self.openai_general)#self.dictionary_lookup)
        Keybinder.bind("<Ctrl><Alt>C", self.thesaurus_lookup)

        Gtk.main()
    
    def on_tray_icon_activate(self, widget):
        print("Tray icon clicked")
        # you can add any action here, like showing/hiding a window

    def on_tray_icon_popup_menu(self, icon, button, time):
        menu = Gtk.Menu()
        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self.quit)
        menu.append(item_quit)
        menu.show_all()
        menu.popup(None, None, None, self.status_icon, button, time)

    def quit(self, widget):
        Gtk.main_quit()

    def translate_text(self, keystring):
        text = self.clipboard_utils.get_selected_text()
        if not text:
            return

        action, translated = self.text_processor.translate(text)
        if translated:
            self.clipboard_utils.set_clipboard_text(translated)
            # self.clipboard_utils.simulate_paste() -- i dont wanna paste after translation
            self.feedback_window.update_content(action, translated)

    def check_text(self, keystring):
        text = self.clipboard_utils.get_selected_text()
        if not text:
            return

        action, corrected = self.text_processor.check_grammar(text)
        if corrected:
            self.clipboard_utils.set_clipboard_text(corrected)
            self.clipboard_utils.simulate_paste()
        self.feedback_window.update_content(action, corrected)

    def openai_general(self, keystring):
        text = self.clipboard_utils.get_selected_text()
        if not text:
            return

        action, response = self.text_processor.general_query(text)
        if response:
            self.clipboard_utils.set_clipboard_text(response)
            self.clipboard_utils.simulate_paste()
        self.feedback_window.update_content(action, response)
        
    
    def search_text(self, keystring):
        text = self.clipboard_utils.get_selected_text()
        if not text:
            return

        action, search_url = self.text_processor.search(text)
        self.feedback_window.update_content(action, f"Searching for: {text}")
        
    def dictionary_lookup(self, keystring):
        word = self.clipboard_utils.get_selected_text()
        if not word:
            return

        action, definition = self.text_processor.dictionary_lookup(word.strip())
        self.feedback_window.update_content(action, definition)
        
    def thesaurus_lookup(self, keystring):
        word = self.clipboard_utils.get_selected_text()
        if not word:
            return

        action, result = self.text_processor.thesaurus_lookup(word.strip())
        self.feedback_window.update_content(action, result)


if __name__ == "__main__":
    app = TextProcessorApp()
    app.run()