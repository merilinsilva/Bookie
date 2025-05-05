###Imports###
import random
import sys
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
#############

# Import the API key
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import YOUTUBE_API_KEY

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_video(genre, test=True, max_results=5):
    # If test is true, then a fixed link will be provided to not exceed the quota
    if test:
        return "lofi hip hop radio 📚 beats to relax/study to", "https://www.youtube.com/watch?v=jfKfPfyJRdk"
    
    # Default to a more general query if the genre isn't mapped
    query = f"{genre.lower()} books playlist"
    
    # Search for playlists using the YouTube Data API
    search_response = youtube.search().list(
        q=query,          # The search term
        part="snippet",   # Include video snippet (title, description, etc.)
        type="playlist",  # Search only for playlists
        maxResults=max_results  # Return multiple results
    ).execute()
    
    # Extract playlists from the response
    if "items" in search_response and search_response["items"]:
        # Randomly select one playlist from the results
        random_item = random.choice(search_response["items"])
        playlist_id = random_item["id"]["playlistId"]
        playlist_title = random_item["snippet"]["title"]
        playlist_link = f"https://www.youtube.com/playlist?list={playlist_id}"
        return playlist_title, playlist_link
    else:
        return None, "No results found."


# # Example usage
# if __name__=='__main__':
#     keyword = "mystery"
#     title, link = search_video(keyword)
#     print(f"Title: {title}")
#     print(f"Link: {link}")