import subprocess
from gi.repository import Gtk, Gdk
import logging

logger = logging.getLogger(__name__)

class ClipboardUtils:
    @staticmethod
    def get_selected_text():
        logger.debug("Getting selected text")
        try:
            return subprocess.check_output(['xsel', '-o']).decode('utf-8')
        except subprocess.CalledProcessError:
            logger.error("Failed to get selected text")
            return None

    @staticmethod
    def set_clipboard_text(text):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)
        clipboard.store()

    @staticmethod
    def simulate_paste():
        subprocess.run(['xdotool', 'key', 'ctrl+v'])