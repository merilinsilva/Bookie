window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");

    loader.classList.add("loader-hidden");

    loader.addEventListener("transitionend", () => {
        loader.remove(); 
    });

    // Dynamic dots logic
    const dots = document.querySelector(".dots");
    let dotCount = 0;

    setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        dots.textContent = ".".repeat(dotCount);
    }, 500); // Update dots every 500ms
});
