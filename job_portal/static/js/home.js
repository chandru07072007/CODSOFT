document.addEventListener('DOMContentLoaded', () => {
    console.log("Home page ready");

    // Optional: Highlight current nav link
    const current = window.location.pathname;
    document.querySelectorAll("nav a").forEach(link => {
        if (link.getAttribute("href") === current) {
            link.style.borderBottom = "2px solid #00f5c6";
        }
    });
});
