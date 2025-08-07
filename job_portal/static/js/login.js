document.addEventListener('DOMContentLoaded', () => {
    console.log("Login page loaded");
});
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent real form submission

        // You can add validation logic here if needed
        // Simulate successful login
        alert("Login successful! Redirecting to home page...");

        // Redirect to home page (adjust URL as needed)
        window.location.href = "/";
    });
});
