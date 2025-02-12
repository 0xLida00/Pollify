document.addEventListener('DOMContentLoaded', function () {
    const addChoiceButton = document.getElementById('add-choice');
    const choicesContainer = document.getElementById('choices-container');
    const choiceTemplate = document.getElementById('choice-template').firstElementChild;

    addChoiceButton.addEventListener('click', () => {
        const newChoice = choiceTemplate.cloneNode(true);
        choicesContainer.appendChild(newChoice);
    });
});