document.addEventListener("DOMContentLoaded", function () {
    const truncateText = (text, wordLimit) => {
        const words = text.split(' ');
        if (words.length > wordLimit) {
            return words.slice(0, wordLimit).join(' ') + '...';
        }
        return text;
    };

    const playlistElement = document.querySelector('.playlist-name');
    if (playlistElement) {
        const fullText = playlistElement.getAttribute('data-full-text');
        playlistElement.textContent = truncateText(fullText, 5);
    }
});