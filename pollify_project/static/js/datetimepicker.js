document.addEventListener('DOMContentLoaded', function () {
    // Select the date input field
    const dateInput = document.querySelector('input[type="datetime-local"]');

    if (dateInput) {
        // Create the "OK" button
        const okButton = document.createElement('button');
        okButton.innerText = 'OK';
        okButton.classList.add('btn', 'btn-success', 'ml-2');

        // Add the button immediately after the input field
        dateInput.parentNode.insertBefore(okButton, dateInput.nextSibling);

        // Hide button initially
        okButton.style.display = 'none';

        // Show button when the input field is focused
        dateInput.addEventListener('focus', function () {
            okButton.style.display = 'inline-block';
        });

        // Handle the "OK" button click
        okButton.addEventListener('click', function () {
            okButton.style.display = 'none'; // Simply hide the button after confirmation
        });
    }
});