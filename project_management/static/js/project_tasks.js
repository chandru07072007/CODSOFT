document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".task-toggle").forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            const taskId = this.closest("li").dataset.taskId;

            fetch(`/toggle_task/${taskId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    if (data.is_done) {
                        this.closest("li").style.textDecoration = "line-through";
                        this.closest("li").style.color = "gray";
                    } else {
                        this.closest("li").style.textDecoration = "none";
                        this.closest("li").style.color = "black";
                    }
                }
            });
        });
    });
});
