"""
This script uses the Hugging Face `facebook/mbart-large-50-many-to-many-mmt` model to translate text
into English, Spanish, and Chinese.
"""

###########Imports##############
from translate import Translator
###########Imports##############

def translate_text(text, source_lang, target_lang):
    """
    Translate text using the `translate` library.

    Args:
        text (str): Input text to translate.
        source_lang (str): Source language code (e.g., "en" for English).
        target_lang (str): Target language code (e.g., "fr" for French).

    Returns:
        str: Translated text.
    """
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translated_text = translator.translate(text)
    return translated_text

# Example Usage
if __name__ == "__main__":
    text = "Life is like a box of chocolates."
    print("English to Portuguese:", translate_text(text, source_lang="en", target_lang="de"))
    print("English to German:", translate_text(text, source_lang="en", target_lang="zh"))