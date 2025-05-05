document.addEventListener("DOMContentLoaded", () => {
    const modeSelect = document.getElementById('mode-select');
    const genreButtons = document.querySelectorAll('.genre-btn');

    // Toggle selection on genre buttons
    if (genreButtons) {
        genreButtons.forEach(button => {
            button.addEventListener('click', () => {
                if (button.classList.contains('selected')) {
                    button.classList.remove('selected');
                } else {
                    button.classList.add('selected');
                }
            });
        });
    }

    // Event listener for mode selection
    if (modeSelect) {
        modeSelect.addEventListener("change", () => {
            const selectedMode = modeSelect.value;

            if (selectedMode === "profile") {
                // Redirect to the template_sel2.py route
                window.location.href = "/profile_selection";
            } else if (selectedMode === "genre") {
                // Redirect back to the sel1 (home) view
                window.location.href = "/";
            }
        });
    }
});