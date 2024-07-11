import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)
        if not self.client.api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise ValueError("OpenAI API key not set")

    def check_grammar(self, text):
        try:
            response = self.client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You're a professional writer. 
                                                 Your task is to correct typos and grammar, keeping the original style of the text. 
                                                 Do not uppercase words that are not written in uppercase in the original text.
                                                                                                  
                                                 Remember to just output the corrected text without any additional words."""},
                {"role": "user", "content": f"Correct the following text: {text}"}
            ])
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in OpenAI grammar check: {e}")
            return None