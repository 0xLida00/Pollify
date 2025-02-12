document.addEventListener("DOMContentLoaded", function () {
    // Ensure WebSocket only initializes on the Poll Detail Page
    const pollContainer = document.getElementById("poll-container");
    if (!pollContainer) return;

    const pollId = pollContainer.getAttribute("data-poll-id");
    const socket = new WebSocket(`ws://${window.location.host}/ws/poll/${pollId}/`);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const choices = data.choices;

        choices.forEach(choice => {
            const progressBar = document.getElementById(`progress-${choice.choice_text}`);
            const voteText = document.getElementById(`choice-${choice.choice_text}`);

            if (progressBar && voteText) {
                progressBar.style.width = `${choice.percentage}%`;
                voteText.innerText = `${choice.percentage.toFixed(2)}% (${choice.votes_count} votes)`;
            }
        });
    };

    socket.onerror = function (error) {
        console.error("WebSocket Error:", error);
    };
});