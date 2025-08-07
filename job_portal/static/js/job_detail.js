document.addEventListener('DOMContentLoaded', () => {
    console.log("Viewing job details...");
});
function saveJob() {
    const job = {
        title: document.getElementById('job-title').textContent,
        company: document.getElementById('job-company').textContent,
        location: document.getElementById('job-location').textContent,
        salary: document.getElementById('job-salary').textContent,
        description: document.getElementById('job-description').textContent
    };

    // Save job data to localStorage
    localStorage.setItem('savedJob', JSON.stringify(job));

    alert("Job saved locally!");
}

// Optional: Load saved job on page load
window.onload = function () {
    const savedJob = localStorage.getItem('savedJob');
    if (savedJob) {
        console.log("Saved Job Found:", JSON.parse(savedJob));
    }
};
