###Imports###
import logging
from openai import OpenAI
import sys
import os
import re
#############

# Import the API key
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENAI_API_KEY

def generate_subgenres_percentages(book_title:str, subgenres: list, abstract: str, test_mode=False) -> list:
    """
    Given a umbrella genre term and the abstract of the book and let the OpenAI API determine their subgenres

    Args:
        book_title (str): involves the title of the book
        subgenres (list): list with possible subgenres of the book's main genre
        abstract (str): the abstract of the according book
        test_mode (bool): To avoid paying for a prompt, when it's for testing purposes
    
    Returns:
        list: Of the subgenres and their percentages in the according book
    """
    try:
        # To not use the API credits I set up a testmode
        # For testing, return a mock response
        if test_mode:
            return {
                "Urban Fantasy": 0.2,
                "Dark Fantasy": 0.0,
                "Magical Realism": 0.4,
                "Mythological Fantasy": 0.1,
                "Children Book": 0.3
            }
        
        # Construct the prompt
        prompt = f"Analyze the abstract ({abstract}) of the book: {book_title} and see from 100% how many percent each genre of the genres: {subgenres} apply to the book's story. Finally, return a string only (no other text) in the format genre1, percentage1/ genre2, percentage2/ etc. Where each genre gets a percentage!!"

        client = OpenAI(
            api_key=OPENAI_API_KEY
        )
        # Request to the OpenAI API
        response = client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        # Now parse the response to get a list of the responses
        response_content = response.choices[0].message.content.strip()

        # Create a dictionary with the genres and their percentages
        genres = re.findall(r'[A-Za-z\s]+(?=\,)', response_content)
        percentages = re.findall(r'\d+\.?\d*(?=%)', response_content)

        subgenre_percentages = {genres[i]: float(percentages[i]) / 100 for i in range(len(genres))}

        return subgenre_percentages
    
    except Exception as e:
        logging.error(f'Error while getting percentages from OpenAI: {e}')
        return []
    
# Test genre
if __name__ == "__main__":
    # Test the function
    print(generate_subgenres_percentages("Alice in Wonderland", ["Urban Fantasy", "Dark Fantasy", "Magical Realism", "Mythological Fantasy", "Children Book"], "Lewis Carroll’s tale Alice’s Adventures in Wonderland is a carnival mirror reflection of Victorian society with its rigid social conventions. While today’s social norms are undoubtedly different from those of Carroll’s time, the story’s underlying challenge still resonates: a child must navigate an unfamiliar world full of arbitrary and ridiculous adult rules, where fear is often the driving force for many participants’ decisions. The answers to riddles are questionable or non-existent. Rote learning offers no guides, tales lack morals. Alice’s good sense and her feeling for justice are indispensable to her success. Through her fantastical adventures, Alice challenges the idea that children should adapt to the adult world with its questionable principles and morality. She finds herself in an imperfect world that can be terrifying, yet her naive but sound judgment helps her survive and unveil the egotism, angst and violence surrounding her. Carroll’s satire of the era, hidden behind fabled creatures absorbed in absurd activities, was so poignant that Queen Victoria herself became Alice’s most eminent fan."))

