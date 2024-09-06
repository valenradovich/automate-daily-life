import os
import requests
import deepl
import langid
import webbrowser
import logging
from services.openai import OpenAIService

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))
        self.openai_service = OpenAIService(os.getenv("OPENAI_API_KEY"))
        self.thesaurus_api_key = os.getenv('MERRIAM_WEBSTER_API_KEY')
        
    def translate(self, text):
        try:
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
        corrected = self.openai_service.check_grammar(text)
        if corrected:
            return "Grammar Check", corrected
        else:
            return "Grammar Check Error", "Failed to check grammar. Please try again."
        
    def general_query(self, prompt):
        response = self.openai_service.general_query(prompt)
        if response:
            return "Response done", response
        else:
            return "OpenAI Error", "Failed to get response. Please try again."

    def search(self, text):
        search_url = f"https://www.google.com/search?q={text}"
        webbrowser.open(search_url)
        return "Web Search", search_url
    
    def dictionary_lookup(self, word):
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if response.status_code == 200:
                data = response.json()[0]
                definitions = []
                for meaning in data['meanings']:
                    part_of_speech = meaning['partOfSpeech']
                    for definition in meaning['definitions']:
                        definitions.append(f"{part_of_speech}: {definition['definition']}")
                
                result = f"Word: {data['word']}\n\nDefinitions:\n" + "\n\n".join(definitions)
                return "Dictionary Lookup", result
            else:
                return "Dictionary Lookup Error", f"No definition found for '{word}'"
        except Exception as e:
            logger.error(f"Dictionary lookup error: {e}")
            return "Dictionary Lookup Error", str(e)
        
    def thesaurus_lookup(self, word):
        if not self.thesaurus_api_key:
            return "Thesaurus Lookup Error", "API key not set"
        
        try:
            url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={self.thesaurus_api_key}"
            response = requests.get(url)
            data = response.json()

            if not data or not isinstance(data[0], dict):
                return "Thesaurus Lookup Error", f"No thesaurus entry found for '{word}'"

            entry = data[0]
            result = f"Word: {word}\n\n"

            if 'meta' in entry and 'syns' in entry['meta']:
                synonyms = [syn for syn_list in entry['meta']['syns'] for syn in syn_list]
                result += "Synonyms:\n" + ", ".join(synonyms) + "\n\n"

            if 'meta' in entry and 'ants' in entry['meta']:
                antonyms = [ant for ant_list in entry['meta']['ants'] for ant in ant_list]
                result += "Antonyms:\n" + ", ".join(antonyms) + "\n\n"

            if 'shortdef' in entry:
                result += "Definitions:\n" + "\n".join(entry['shortdef'])

            return "Thesaurus Lookup", result
        except Exception as e:
            logger.error(f"Thesaurus lookup error: {e}")
            return "Thesaurus Lookup Error", str(e)