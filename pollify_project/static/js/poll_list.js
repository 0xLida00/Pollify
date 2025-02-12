document.addEventListener("DOMContentLoaded", function () {
    const deletePollModal = $("#deletePollModal");
    const deletePollForm = document.getElementById("deletePollForm");

    if (!deletePollModal || !deletePollForm) {
        console.error("Modal or form not found.");
        return;
    }

    // Handle the modal show event
    deletePollModal.on("show.bs.modal", function (event) {
        const button = $(event.relatedTarget);

        if (!button) {
            console.error("No related button found for modal.");
            return;
        }

        const pollUrl = button.data("poll-url");

        if (!pollUrl) {
            console.error("Poll URL is missing in button attributes.");
            return;
        }

        deletePollForm.setAttribute("action", pollUrl);
    });
});