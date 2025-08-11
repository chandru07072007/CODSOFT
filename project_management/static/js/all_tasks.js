// all_tasks.js
// Handles toggling tasks via checkbox clicks on the all tasks page

document.addEventListener('DOMContentLoaded', function() {
    const taskList = document.getElementById('all-task-list');
    if (!taskList) return;
    taskList.addEventListener('change', function(e) {
        if (e.target.classList.contains('task-toggle')) {
            const li = e.target.closest('li[data-task-id]');
            const taskId = li.getAttribute('data-task-id');
            if (taskId) {
                window.location.href = `/toggle_task/${taskId}`;
            }
        }
    });
});
