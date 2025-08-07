document.addEventListener('DOMContentLoaded', () => {
    console.log("Employer dashboard ready.");

    // Highlight all job cards
    const jobCards = document.querySelectorAll('.job-card');
    jobCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.backgroundColor = '#e6f0ff';
            card.style.cursor = 'pointer';
        });

        card.addEventListener('mouseleave', () => {
            card.style.backgroundColor = '#f0f4ff';
        });
    });

    // Toggle applications visibility
    const toggleBtn = document.getElementById('toggle-applications');
    const appSection = document.getElementById('application-section');

    if (toggleBtn && appSection) {
        toggleBtn.addEventListener('click', () => {
            if (appSection.style.display === 'none') {
                appSection.style.display = 'block';
                toggleBtn.textContent = 'Hide Applications';
            } else {
                appSection.style.display = 'none';
                toggleBtn.textContent = 'Show Applications';
            }
        });
    }
});
