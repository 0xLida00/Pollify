document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".follow-form").forEach((form) => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const button = form.querySelector("button");
            const csrfToken = this.querySelector("input[name=csrfmiddlewaretoken]").value;

            // Disable the button to prevent multiple clicks
            button.disabled = true;

            fetch(this.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        // Update the button's appearance based on the new state
                        if (data.action === "follow") {
                            button.classList.remove("btn-success");
                            button.classList.add("btn-danger");
                            button.textContent = "Unfollow";
                        } else {
                            button.classList.remove("btn-danger");
                            button.classList.add("btn-success");
                            button.textContent = "Follow";
                        }
                    } else {
                        alert("An error occurred. Please try again.");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                })
                .finally(() => {
                    // Re-enable the button after the request completes
                    button.disabled = false;
                });
        });
    });
});