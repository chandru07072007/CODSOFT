// script.js
// Add your JavaScript here
document.addEventListener("DOMContentLoaded", function () {
    const taskList = document.querySelectorAll("ul li");

    // Fade-out animation when toggling task
    taskList.forEach(li => {
        const checkbox = li.querySelector("input[type='checkbox']");
        checkbox.addEventListener("change", function () {
            li.classList.add("fade-out");
            setTimeout(() => {
                window.location.href = checkbox.getAttribute("onclick").match(/'(.*?)'/)[1];
            }, 300); // Delay before redirect
        });
    });

    // Highlight newly added task (if any)
    const newTask = document.querySelector("ul li:first-child");
    if (newTask && !newTask.classList.contains("done")) {
        newTask.classList.add("highlight");
        setTimeout(() => {
            newTask.classList.remove("highlight");
        }, 1500);
    }
});
