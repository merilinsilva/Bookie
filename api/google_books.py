###Imports###
import random
import requests
import logging
import sys
import os
#############

# Import the API key
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import GOOGLE_BOOKS_API_KEY

base_url = "https://www.googleapis.com/books/v1/volumes"

def search_books_by_genre(genres, total_books=5, search_limit=30):
    """
    Search for books by genres, fetch a specified number of total random books from the results.

    Args:
        genres (list): List of umbrella genres to search.
        total_books (int): Number of books to return for each genre.
        search_limit (int): Number of books to fetch from the API per genre.

    Returns:
        dict: Dictionary of books containing title, authors, cover image, abstract, etc.
    """
    # Initialize a dictionary to hold all the books from all genres
    all_books = {}

    # Loop through each genre to fetch books
    for genre in genres:
        # Set up the parameters for the Google Books API request
        params = {
            "q": f"subject:{genre}",  # Search for books by subject (genre)
            "maxResults": search_limit,  # Limit the number of results to fetch
            "key": GOOGLE_BOOKS_API_KEY  # Include the API key
        }

        try:
            # Send the GET request to the Google Books API
            response = requests.get(base_url, params=params)
            
            # Raise an HTTPError if the response contains an error status code
            response.raise_for_status()

            data = response.json()
            # Process the raw data to extract the necessary book details
            books_data = process_books_data(data, genre)
            
            # Randomly select 'total_books' from the processed books
            # Use random.sample to ensure random selection without duplication
            selected_books = random.sample(list(books_data.values()), min(total_books, len(books_data)))
            
            # Add the selected books to the final collection
            for book in selected_books:
                all_books[book["title"]] = book
        
        # Handle any exceptions that occur during the API request
        except requests.RequestException as e:
            logging.error(f"Error fetching data from Google Books API for genre '{genre}': {e}")

    return all_books

    
def process_books_data(data, genre):
    """
    Process the raw data from Google Books API to extract necessary details.

    Args:
        data (dict): JSON response from Google Books API.

    Returns:
        list: A list of dictionaries containing title, authors, cover image, and abstract. The ID is the book title.
    """
    books = {}
    # Gets the data of the books
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        book = {
            "title": volume_info.get("title", "No title available"),
            "authors": volume_info.get("authors", ["Unknown author"]),
            "cover_image": volume_info.get("imageLinks", {}).get("thumbnail", ""),
            "abstract": volume_info.get("description", "No description available"),
            "rating": volume_info.get("averageRating", "No rating available"),
            "umbrella_genre": genre
        }
        books[book["title"]] = book

    return books

# if __name__ == "__main__":
#     # Test the function
#     test_genres = ["Science Fiction", "Romance"]
#     books = search_books_by_genre(test_genres)
#     print(books.items())
