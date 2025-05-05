document.addEventListener("DOMContentLoaded", function () {
    const truncateText = (text, wordLimit) => {
        const words = text.split(' ');
        if (words.length > wordLimit) {
            return words.slice(0, wordLimit).join(' ') + '...';
        }
        return text;
    };

    document.querySelectorAll('.book-description').forEach(desc => {
        const fullText = desc.getAttribute('data-full-text');
        desc.textContent = truncateText(fullText, 20);
    });
});