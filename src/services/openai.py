from openai import OpenAI
import logging
from gi.repository import Gtk, Gdk
from utils.clipboard_utils import ClipboardUtils

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)
        if not self.client.api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise ValueError("OpenAI API key not set")

    def check_grammar(self, text):
        try:
            response = self.client.chat.completions.create(model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You're a professional writer. 
                                                 Your task is to correct typos and grammar, keeping the original style of the text. 
                                                 Do not capitalize letters that were not capitalized and do not include a period if it was not in the original text.
                                                                                                  
                                                 Remember to just output the corrected text without any additional words."""},
                {"role": "user", "content": f"Correct the following text: {text}"}
            ])
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in OpenAI grammar check: {e}")
            return None
            
    def general_query(self, prompt):
        try:
            # collected_text = ''
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a helpful assistant. Provide informative and concise responses.
                                                    Always output the user's prompt at the beggining of your response."""},
                    {"role": "user", "content": prompt}],
                # stream=True
            )
            return response.choices[0].message.content.strip()
            # for chunk in response:
            #     # print("THIS IS A CHUNKKKKKKKKKKKKKK: ", chunk)
            #     if chunk.choices[0].delta.content:
            #         token = chunk.choices[0].delta.content
            #         print(token)
            #         # Append it to the collected text
            #         collected_text += token
                    
            #         # Update the clipboard with the growing text and simulate paste
            #         ClipboardUtils.set_clipboard_text(collected_text)
            #         ClipboardUtils.simulate_paste()
                    
            #         # Print the token to console (optional for debugging)
            #         print(token, end='', flush=True)
        except Exception as e:
            logger.error(f"Error in OpenAI general query: {e}")
            return "Error", str(e)