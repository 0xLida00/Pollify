document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded. Adding comment voting event listeners.");

    document.querySelectorAll(".comment-vote").forEach((button) => {
        button.addEventListener("click", function () {
            console.log("Vote button clicked.");

            const commentId = this.getAttribute("data-comment-id");
            const action = this.getAttribute("data-action");
            const upvoteCount = document.getElementById(`upvote-count-${commentId}`);
            const downvoteCount = document.getElementById(`downvote-count-${commentId}`);
            const url = `/comments/comment/${commentId}/${action}/`;

            console.log(`Sending request to: ${url}`);

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
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
                    console.log("Response received:", data);

                    if (data.success) {
                        // Update vote counts
                        upvoteCount.innerText = data.upvotes;
                        downvoteCount.innerText = data.downvotes;

                        // Remove previous vote highlight
                        document.querySelectorAll(`button[data-comment-id="${commentId}"]`).forEach((btn) => {
                            btn.classList.remove("btn-success", "btn-danger");
                        });

                        // Highlight current vote
                        if (action === "upvote") {
                            this.classList.add("btn-success");
                        } else {
                            this.classList.add("btn-danger");
                        }
                    } else {
                        console.warn("Vote action failed:", data.message);
                    }
                })
                .catch((error) => {
                    console.error("Error sending vote:", error);
                });
        });
    });
});