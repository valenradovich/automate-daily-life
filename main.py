import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Keybinder', '3.0')
from gi.repository import Gtk, Gdk, GLib, Keybinder
import langdetect
import deepl
import language_tool_python
import subprocess
import os
from dotenv import load_dotenv
import logging
import webbrowser

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FeedbackWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Text Processor Feedback")
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

    def update_content(self, action, result):
        self.action_label.set_text(action)
        self.result_buffer.set_text(result)
        self.show_all()
        GLib.timeout_add_seconds(25, self.hide)

    def on_delete_event(self, widget, event):
        self.hide()
        return True  

class TextProcessorApp:
    def __init__(self):
        logger.info("Initializing Text Processor App")
        self.translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))
        self.language_tool = language_tool_python.LanguageTool('en-US')
        self.feedback_window = FeedbackWindow()

    def run(self):
        logger.info("Running Text Processor App")
        Keybinder.init()
        Keybinder.bind("<Ctrl>Q", self.translate_text)
        Keybinder.bind("<Ctrl>D", self.check_text)
        Keybinder.bind("<Ctrl>S", self.search_text)

        Gtk.main()

    def get_selected_text(self):
        logger.debug("Getting selected text")
        try:
            return subprocess.check_output(['xsel', '-o']).decode('utf-8')
        except subprocess.CalledProcessError:
            logger.error("Failed to get selected text")
            return None

    def set_clipboard_text(self, text):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)
        clipboard.store()

    def translate_text(self, keystring):
        text = self.get_selected_text()
        if not text:
            return

        try:
            detected_lang = langdetect.detect(text)
            if detected_lang == 'en':
                translated = self.translator.translate_text(text, target_lang="ES")
                action = "Translated from English to Spanish"
            elif detected_lang == 'es':
                translated = self.translator.translate_text(text, target_lang="EN-US")
                action = "Translated from Spanish to English"
            else:
                logger.warning(f"Unsupported language detected: {detected_lang}")
                return

            self.set_clipboard_text(str(translated))
            self.simulate_paste()
            self.feedback_window.update_content(action, str(translated))
        except deepl.exceptions.DeepLException as e:
            logger.error(f"DeepL translation error: {e}")
            self.feedback_window.update_content("Translation Error", str(e))

    def check_text(self, keystring):
        text = self.get_selected_text()
        if not text:
            return

        matches = self.language_tool.check(text)
        if matches:
            corrected = language_tool_python.utils.correct(text, matches)
            self.set_clipboard_text(corrected)
            self.simulate_paste()
            self.feedback_window.update_content("Grammar Check", corrected)
        else:
            self.feedback_window.update_content("Grammar Check", "No grammar or spelling issues found.")
            
    def search_text(self, keystring):
        text = self.get_selected_text()
        if not text:
            return

        search_url = f"https://www.google.com/search?q={text}"
        webbrowser.open(search_url)
        self.feedback_window.update_content("Web Search", f"Searching for: {text}")

    def simulate_paste(self):
        subprocess.run(['xdotool', 'key', 'ctrl+v'])

if __name__ == "__main__":
    app = TextProcessorApp()
    app.run()