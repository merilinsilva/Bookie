##########Imports#####################################################################################
import uuid
import json
import os
import random
from urllib.parse import unquote
from flask import Flask, render_template, url_for, redirect, request, jsonify, session
from flask_login import login_user,  LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from data_processing.data_processing import process_chosen_data
from models import db, User, Library, SubgenrePlot
from data_processing.translate_text import translate_text
##########Imports#####################################################################################

#############################Set up flash and configure data base###################################################################
app = Flask(__name__)
# Connect app file to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:268242e9deb88b04451d19716526a9b2@172.23.66.239:59839/team_project_5_db'
# Create key
app.config['SECRET_KEY'] = 'gvevjkwhwhyf35796'
# Initialize SQLAlchemy with app
db.init_app(app)
# To hash passwords
bcrypt = Bcrypt(app)
#############################Set up flash and configure data base###################################################################


#########################################Set up login, register and logout################################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Validation form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"}) # since we don't know how large the parsed hash will be, we set it to 80 above
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        # query database table to search for existing usernames
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

# Login form
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"}) # since we don't know how large the parsed hash will be, we set it to 80 above
    
    submit = SubmitField("Login")
#########################################Set up login, register and logout################################################

####################################Define the routs of the websites############################
'''
Content:
- Main Page
- Main Page when selecting 'by Profile'
- Register Website
- Login Website
- Logout Website
- Process getting genres
- Book Recommendations Website
- Book Details Website
- Get genres from library content
- Library Website
- Library Book Details Website
- Add Books to Library
- Remove Books from Library
- About Website
'''
################### Independent Function that Removes Temporary BookInfo File#########
def delete_temp_file():
    recommendation_id = session.get("recommendation_id")
    if recommendation_id:
        temp_file_path = os.path.join(TEMP_STORAGE_PATH, f"{recommendation_id}.json")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        session.pop("recommendation_id", None)  # Remove from session
################### Independent Function that Removes Temporary BookInfo File#########

##############Main Website##################
@app.route("/")
def home():
    delete_temp_file() # If one goes to the main page, the book file gets deleted
    return render_template("template_sel1.html")
##############Main Website##################

################Main Page with Profile Selection################
@app.route("/profile_selection")
def sel_profile():
    return render_template("template_sel2.html")
################Main Page with Profile Selection################

###############Check if user is logged in######################
@app.route("/is-logged-in", methods=["GET"])
def is_logged_in():
    return jsonify({"logged_in": current_user.is_authenticated})
###############Check if user is logged in######################

###################Register Website###########################
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm() # Initialize RegisterForm

    if form.validate_on_submit():
        # hashes password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # creates new user
        new_user = User(username=form.username.data, password=hashed_password)
        # add user to database
        db.session.add(new_user)
        db.session.commit()
        # redirect to login page
        return redirect(url_for('login'))
    return render_template("template_register.html", form=form)
###################Register Website###########################

#############Login Website##################
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    # Validate Login
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Check password
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('library'))
    # If login is not valid, render again Login Website
    return render_template("template_login.html", form=form) 
#############Login Website##################

############Logout that redirects to login#########
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # If one logs out, the Book Information in the temporary file gets deleted
    delete_temp_file()
    logout_user()
    return redirect(url_for('login'))
############Logout that redirects to login#########

###########Handles translations#######################
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")
    source_lang = data.get("source_lang", "en")  # Default source language
    target_lang = data.get("target_lang", "en")  # Default target language

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        translated_text = translate_text(text, source_lang, target_lang)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
###########Handles translations#######################

###########Handle Getting Genres and Returning Recommendation#################################
TEMP_STORAGE_PATH = "data_processing/temp_recommendations"  # Directory for temporary data storage
os.makedirs(TEMP_STORAGE_PATH, exist_ok=True)  # Ensure the directory exists

@app.route("/process-genres", methods=["POST"])
def process_genres():
    # Get the chosen Genres
    data = request.json
    genres = data.get("genres", [])
    if not genres:
        return jsonify({"error": "No genres provided"}), 400

    # Process chosen genres to get book recommendations
    book_data = process_chosen_data(genres)

    # Generate a unique ID for this set of recommendations
    recommendation_id = str(uuid.uuid4())

    # Save the recommendations to a temporary file
    temp_file_path = os.path.join(TEMP_STORAGE_PATH, f"{recommendation_id}.json")
    with open(temp_file_path, "w") as temp_file:
        json.dump(book_data, temp_file)

    # Store the ID in the session (small size)
    session["recommendation_id"] = recommendation_id

    return jsonify({"redirect": url_for("book_recommendations")})
###########Handle Getting Genres and Returning Recommendation#################################


###########Book Recommendation Website#########################################
@app.route("/book_recommendations")
def book_recommendations():
    # Retrieve the recommendation ID from the session
    recommendation_id = session.get("recommendation_id")

    if not recommendation_id:
        return redirect(url_for("home"))  # Redirect if no recommendations

    # Load the recommendations from the temporary file
    temp_file_path = os.path.join(TEMP_STORAGE_PATH, f"{recommendation_id}.json")
    if not os.path.exists(temp_file_path):
        return redirect(url_for("home"))  # Redirect if file is missing

    with open(temp_file_path, "r") as temp_file:
        recommendations = json.load(temp_file)

    return render_template("template_book-recs.html", recommendations=recommendations)
###########Book Recommendation Website#########################################

################General Book Details Website####################
@app.route("/book/<book_id>")
def book_details(book_id):
    # Load the recommendation data from the temporary file
    temp_file_path = os.path.join(TEMP_STORAGE_PATH, f"{session['recommendation_id']}.json")
    with open(temp_file_path, "r") as temp_file:
        recommendations = json.load(temp_file)

    # Find the book by ID
    book = recommendations.get(book_id)
    if not book:
        return "Book not found", 404
    # Pass the book details to the template
    return render_template("template_book-det.html", book=book)
################General Book Details Website####################

################### Use Profile Genres for Book Recommendations#######################
@app.route("/process-profile", methods=["POST"])
def process_profile():
    # Check if the user is logged in
    if not current_user.is_authenticated:
        return jsonify({"error": "For this function, you need to be logged in."}), 401  # 401 Unauthorized
    
    # Fetch all books belonging to the current user
    user_books = Library.query.filter_by(user_id=current_user.id).all()

    if not user_books:
        return jsonify({"error": "No books stored in your library."}), 400

    # Extract up to two unique umbrella genres from the user's library
    umbrella_genres = list(set([book.umbrella_genre for book in user_books if book.umbrella_genre]))
    # Randomly select up to two genres from the available list
    selected_genres = random.sample(umbrella_genres, min(2, len(umbrella_genres)))

    # If no genres are found, return an error
    if not selected_genres:
        return jsonify({"error": "No valid genres found in your library."}), 400

    # Process selected genres to generate book recommendations
    book_data = process_chosen_data(selected_genres)

    # Generate a unique ID for storing these recommendations
    recommendation_id = str(uuid.uuid4())

    # Save recommendations in a temporary JSON file
    temp_file_path = os.path.join(TEMP_STORAGE_PATH, f"{recommendation_id}.json")
    with open(temp_file_path, "w") as temp_file:
        json.dump(book_data, temp_file)

    # Store the recommendation ID in the session
    session["recommendation_id"] = recommendation_id

    return jsonify({"redirect": url_for("book_recommendations")})
################### Use Profile Genres for Book Recommendations#######################

############Library Website#####################################
@app.route('/library', methods=['GET'])
@login_required
def library():
    # Fetch books from the current user's library
    books = Library.query.filter_by(user_id=current_user.id).all()
    return render_template('template_library.html', books=books)
############Library Website#####################################

################Library Book Details Website####################
@app.route('/library/book/<int:book_id>', methods=['GET'])
@login_required
def library_book_details(book_id):
    # Fetch the specific book from the user's library
    book = Library.query.filter_by(id=book_id, user_id=current_user.id).first()
    if not book:
        return "Book not found", 404
    return render_template('template_library_book-det.html', book=book)
################Library Book Details Website####################

################Add to Library############################
@app.route("/add-to-library/<book_title>", methods=["POST"])
@login_required
def add_to_library(book_title):
    # Decode the URL-encoded title
    book_title = unquote(book_title)

    # Load the recommendation data
    temp_file_path = os.path.join(TEMP_STORAGE_PATH, f"{session['recommendation_id']}.json")
    if not os.path.exists(temp_file_path):
        return jsonify({"error": "Recommendations file not found"}), 500

    with open(temp_file_path, "r") as temp_file:
        recommendations = json.load(temp_file)

    # Find the book by title
    book = recommendations.get(book_title)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Convert list fields to strings
    subgenres_str = ", ".join(book.get("subgenres", []))  # Convert subgenres list to a comma-separated string

    # Save the book to the user's library
    library_entry = Library(
        user_id=current_user.id,
        book_title=book["title"],
        book_authors=", ".join(book["authors"]),  # Convert authors list to a comma-separated string
        book_cover=book["cover_image"],
        book_description=book["abstract"],  # Match the correct field in the JSON
        book_rating=book["rating"] if isinstance(book.get("rating"), (int, float)) else 0.0,
        book_playlist=book.get("playlist"),
        book_playlistname=book.get("playlist_name"),
        umbrella_genre=book.get("umbrella_genre"),
        subgenres=subgenres_str,  # Save the converted string
        percentages=book["percentages"],  # Ensure it's a string
    )
    db.session.add(library_entry)
    db.session.commit()

    return jsonify({"message": "Book added to library successfully."})
################Add to Library############################

#######################Remove from Library###################################
@app.route("/remove-from-library/<int:book_id>", methods=["POST"])
@login_required
def remove_from_library(book_id):
    # Find the book in the current user's library
    book = Library.query.filter_by(id=book_id, user_id=current_user.id).first()

    if not book:
        return jsonify({"error": "Book not found or you don't have permission to remove it."}), 404

    # Remove the book from the library
    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book successfully removed from your library."})
#######################Remove from Library###################################

##########################About Website###########
@app.route("/about")
def about():
    return render_template("template_about.html")
##########################About Website###########
####################################Define the routs of the websites############################

###################Load Server Locally#########################
if __name__ == "__main__":
    with app.app_context():
            print("Deleting all entries in subgenre_plots...")
            db.session.query(SubgenrePlot).delete()
            db.session.commit()
    app.run(host="0.0.0.0", port=5000, debug=True)
###################Load Server Locally#########################
