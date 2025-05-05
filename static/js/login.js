document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === "testuser" && password === "password123") {
        alert("Login successful!");
        window.location.href = "library.html"; // Redirect to the library page
    } else {
        alert("Invalid username or password. Please try again.");
    }
});