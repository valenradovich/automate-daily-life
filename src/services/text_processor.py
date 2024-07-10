import os
import deepl
# import langdetect
import langid
import language_tool_python
import webbrowser
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))
        self.language_tool = language_tool_python.LanguageTool('en-US')
        
    def translate(self, text):
        try:
            # detected_lang = langdetect.detect_langs(text)
            langid.set_languages(['en','es'])
            detected_lang, score = langid.classify(text)
            print(detected_lang)
            if detected_lang == 'en':
                translated = self.translator.translate_text(text, target_lang="ES")
                action = "Translated from English to Spanish"
            elif detected_lang == 'es':
                translated = self.translator.translate_text(text, target_lang="EN-US")
                action = "Translated from Spanish to English"
            else:
                logger.warning(f"Unsupported language detected: {detected_lang}")
                return "Translation Error", f"Unsupported language: {detected_lang}"

            return action, str(translated)
        except deepl.exceptions.DeepLException as e:
            logger.error(f"DeepL translation error: {e}")
            return "Translation Error", str(e)

    def check_grammar(self, text):
        matches = self.language_tool.check(text)
        if matches:
            corrected = language_tool_python.utils.correct(text, matches)
            return "Grammar Check", corrected
        else:
            return "Grammar Check", "No grammar or spelling issues found."

    def search(self, text):
        search_url = f"https://www.google.com/search?q={text}"
        webbrowser.open(search_url)
        return "Web Search", search_url