document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Stop actual submission
        alert("Login successful! Redirecting to home page...");
        window.location.href = "/"; // Redirect to home page
    });
});
