document.addEventListener("DOMContentLoaded", () => {
    const genreButtons = document.querySelectorAll(".genre-btn");
    const findBookBtn = document.querySelector(".find-book-btn");
    const modeSelect = document.querySelector("#mode-select");
    const selectedGenres = [];

    // Toggle genres on button click
    genreButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const genre = button.textContent.trim();
            if (selectedGenres.includes(genre)) {
                selectedGenres.splice(selectedGenres.indexOf(genre), 1);
                button.classList.remove("selected");
            } else {
                selectedGenres.push(genre);
                button.classList.add("selected");
            }
        });
    });

    // Fetch book recommendations based on mode selection
    findBookBtn.addEventListener("click", async () => {
        const selectedMode = modeSelect.value;

        if (selectedMode === "genre") {
            if (selectedGenres.length === 0) {
                alert("Please select at least one genre!");
                return;
            }

            try {
                // Send selected genres to the backend
                const response = await fetch("/process-genres", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ genres: selectedGenres }),
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.redirect) {
                        // Redirect to the book list page
                        window.location.href = data.redirect;
                    }
                } else {
                    console.error("Failed to fetch book recommendations.");
                    alert("Something went wrong while processing your request. Please try again.");
                }
            } catch (error) {
                console.error("Error occurred while fetching recommendations:", error);
                alert("An error occurred. Please check your internet connection and try again.");
            }
        } else if (selectedMode === "profile") {
            // Fetch recommendations based on the user's profile
            try {
                const response = await fetch("/process-profile", {
                    method: "POST",
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                } else {
                    const errorData = await response.json();
                    alert(errorData.error || "Failed to fetch profile-based recommendations.");
                }
            } catch (error) {
                console.error("Error occurred while fetching profile-based recommendations:", error);
                alert("An error occurred. Please try again.");
            }
        }
    });

    // Dynamically populate recommendations
    function populateRecommendations(data) {
        const bookContainer = document.getElementById("book-recommendations");
        if (!bookContainer) {
            console.error("Book container not found on the page.");
            return;
        }

        bookContainer.innerHTML = ""; // Clear previous recommendations

        Object.keys(data).forEach((bookId) => {
            const book = data[bookId];
            const bookHTML = `
              <div class="book-recommendation">
                <img src="${book.cover_image}" alt="${book.title}" class="book-cover" />
                <div class="book-details">
                  <h3>${book.title}</h3>
                  <p><strong>Author:</strong> ${book.authors.join(", ")}</p>
                  <p>${book.abstract}</p>
                  <p><strong>Rating:</strong> ⭐ ${book.rating}</p>
                  <p><strong>Subgenres:</strong> ${book.subgenres.join(", ")}</p>
                  <img src="${book.percentages}" alt="Subgenre Percentages" class="genre-chart" />
                  <a href="/book/${bookId}" class="details-button">See more details</a>
                </div>
              </div>
            `;
            bookContainer.insertAdjacentHTML("beforeend", bookHTML);
        });
    }

    // Add event listeners to dynamically added "See More Details" buttons
    function handleDetailsButtonClicks() {
        const detailsButtons = document.querySelectorAll(".details-button");
        detailsButtons.forEach((button) => {
            button.addEventListener("click", (e) => {
                e.preventDefault(); // Prevent default anchor behavior
                const bookId = button.getAttribute("href").split("/").pop();
                window.location.href = `/book/${bookId}`;
            });
        });
    }
});
