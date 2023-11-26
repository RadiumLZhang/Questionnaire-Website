// script.js

document.addEventListener('DOMContentLoaded', function() {
    var consentRadios = document.querySelectorAll('input[name="consent"]');
    var eligibilityRadios = document.querySelectorAll('input[name="eligibility"]');

    // Adding event listeners to the radio buttons
    consentRadios.forEach(function(radio) {
        radio.addEventListener('change', updateButtonState);
    });

    eligibilityRadios.forEach(function(radio) {
        radio.addEventListener('change', updateButtonState);
    });


    // Handling form submission
    surveyForm.addEventListener('submit', function(event) {

        event.preventDefault(); // Prevent default form submission behavior

        // Redirect to survey_id_entry.html
        window.location.href = '/survey_id_entry';
    });

    // Hide the tooltip when clicking anywhere else
    document.addEventListener('click', function(event) {
        var tooltip = document.getElementById("tooltip");
        if (!tooltip.contains(event.target) && event.target.className !== 'help-icon') {
            tooltip.style.display = 'none';
        }
    });

    document.getElementById("tooltip").addEventListener('click', function(event) {
        event.stopPropagation();
    });


    // Initial check in case the form is pre-filled or cached
    updateButtonState();
});


// Function to check the state of the radio buttons and update the button's disabled state
function updateButtonState() {

    var submitButton = document.getElementById('submitButton');
    var tooltip = document.getElementById('tooltip');
    var helpIcon = document.querySelector(".help-icon");

    var consentGiven = document.querySelector('input[name="consent"]:checked')?.value === 'Yes';
    var isEligible = document.querySelector('input[name="eligibility"]:checked')?.value === 'Yes';

    submitButton.disabled = !(consentGiven && isEligible);
    tooltip.style.display = 'none'; // Hide tooltip when state is updated
    helpIcon.style.display = submitButton.disabled ? 'inline-block' : 'none';
}


function showHelp() {
    var tooltip = document.getElementById("tooltip");
    tooltip.style.display = tooltip.style.display === 'block' ? 'none' : 'block';
}