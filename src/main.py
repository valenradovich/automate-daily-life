import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Keybinder', '3.0')
from gi.repository import Gtk, Keybinder
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

    def run(self):
        logger.info("Running Text Processor App")
        Keybinder.init()
        Keybinder.bind("<Ctrl><Alt>Q", self.translate_text)
        Keybinder.bind("<Ctrl><Alt>G", self.check_text)
        Keybinder.bind("<Ctrl><Alt>S", self.search_text)
        Keybinder.bind("<Ctrl><Alt>C", self.dictionary_lookup)
        Keybinder.bind("<Ctrl><Alt>A", self.thesaurus_lookup)

        Gtk.main()

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