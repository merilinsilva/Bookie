#####Imports#####
import json
import random
import os
import sys
from models import db, SubgenrePlot

# Add the parent directory of 'api' to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.openai_genres import generate_subgenres_percentages
from api.google_books import search_books_by_genre
from api.youtube_playlist import search_video
from data_processing.create_plot import create_percentage_plot
#################
def process_chosen_data(genre_list):
    # Get the books for the given genres
    book_information = search_books_by_genre(genre_list, 5)

    # Load subgenres from the JSON file
    with open("data_processing/genres.json", "r") as f:
        genre_dict = json.load(f)

    for genre in genre_list:
        for book in book_information.items():
            book_title = book[1]["title"]

            # Generate subgenres and percentages
            subgenres = genre_dict[genre]
            
            # Check if the plot already exists in the database
            existing_plot = SubgenrePlot.query.filter_by(book_title=book_title).first()

            if existing_plot:
                # Use the existing plot data
                book[1]["percentages"] = existing_plot.plot_data
            else:
                # Generate percentages of subgenres
                percentages = generate_subgenres_percentages(book_title, subgenres, book[1]["abstract"])

                # Skip books with empty percentages
                if not percentages:
                    continue

                # Create the plot
                plot_data = create_percentage_plot(percentages)
                book[1]["percentages"] = plot_data

                # Add to the SubgenrePlot table
                new_plot = SubgenrePlot(book_title=book_title, plot_data=plot_data)
                db.session.add(new_plot)
                db.session.commit()

            # Add subgenre details to the book
            video_title, video_link = search_video(random.choice(subgenres))
            book[1]["playlist"] = video_link
            book[1]["playlist_name"] = video_title
            book[1]["subgenres"] = subgenres

    return book_information


if __name__ == "__main__":
    # Test the function
    print(process_chosen_data(['Mystery', 'Fantasy']))