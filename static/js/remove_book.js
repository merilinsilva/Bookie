document.addEventListener("DOMContentLoaded", () => {
    const removeBookButton = document.querySelector(".remove-book-btn");

    // Handle the Remove button click
    removeBookButton.addEventListener("click", async () => {
        // Get the book ID from the URL (assuming the book ID is part of the URL)
        const bookId = window.location.pathname.split("/").pop();

        try {
            const response = await fetch(`/remove-from-library/${bookId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            if (response.ok) {
                alert("Book successfully removed from your library!");
                // Redirect back to the library
                window.location.href = "/library";
            } else {
                const errorData = await response.json();
                alert(`Failed to remove the book: ${errorData.error}`);
            }
        } catch (error) {
            console.error("Error removing book from library:", error);
            alert("An error occurred. Please try again.");
        }
    });
});