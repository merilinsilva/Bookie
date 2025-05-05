document.addEventListener("DOMContentLoaded", () => {
    const plotContainers = document.querySelectorAll(".plot-container img");

    plotContainers.forEach((plot) => {
        plot.style.width = "700px"; // Set the desired width
        plot.style.height = "400px"; // Set the desired height
        plot.style.objectFit = "contain"; // Ensure aspect ratio is maintained
    });
});
