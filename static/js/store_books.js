document.addEventListener("DOMContentLoaded", () => {
    const addToLibraryButton = document.querySelector(".add-to-library");

    // Handle the Add to Library button click
    addToLibraryButton.addEventListener("click", async () => {
        try {
            // Check if the user is logged in
            const loginResponse = await fetch("/is-logged-in");
            const loginData = await loginResponse.json();

            if (!loginData.logged_in) {
                alert("To store books in your library, you need to be logged in.");
                return; // Stop execution if the user is not logged in
            }

            // Extract the book title (assuming the structure: "Title" by Author)
            const bookId = document.querySelector("h1").textContent.trim().split(" by ")[0].replace(/"/g, "");

            // Proceed to add the book to the library
            const response = await fetch(`/add-to-library/${encodeURIComponent(bookId)}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            if (response.ok) {
                alert("Book successfully added to your library!");
            } else {
                const errorData = await response.json();
                alert(`Failed to add the book to your library: ${errorData.error}`);
            }
        } catch (error) {
            console.error("Error adding book to library:", error);
            alert("An error occurred. Please try again.");
        }
    });
});
