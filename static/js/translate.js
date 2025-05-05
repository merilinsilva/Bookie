document.addEventListener("DOMContentLoaded", () => {
    const translateLinks = document.querySelectorAll(".translate-link");
    const descriptionContainer = document.getElementById("book-description");

    // Set initial language as English
    descriptionContainer.setAttribute("data-lang", "en");

    translateLinks.forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();
            const targetLang = link.getAttribute("data-lang");
            const currentLang = descriptionContainer.getAttribute("data-lang");
            const text = descriptionContainer.textContent;

            // Prevent translating into the same language
            if (currentLang === targetLang) {
                alert("The text is already in the selected language.");
                return;
            }

            fetch("/translate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    source_lang: currentLang, // Use the current language
                    target_lang: targetLang
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.translated_text) {
                    descriptionContainer.textContent = data.translated_text;
                    descriptionContainer.setAttribute("data-lang", targetLang); // Update the current language
                } else {
                    alert("Translation failed: " + (data.error || "Unknown error"));
                }
            })
            .catch(error => {
                console.error("Error translating text:", error);
                alert("An error occurred while translating the text.");
            });
        });
    });
});
