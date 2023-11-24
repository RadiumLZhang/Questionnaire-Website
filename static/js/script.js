// script.js

document.addEventListener('DOMContentLoaded', function() {
    var consentRadios = document.querySelectorAll('input[name="consent"]');
    var eligibilityRadios = document.querySelectorAll('input[name="eligibility"]');
    var submitButton = document.getElementById('submitButton');

    // Function to check the state of the radio buttons and update the button's disabled state
    function updateButtonState() {
        var consentGiven = document.querySelector('input[name="consent"]:checked')?.value === 'Yes';
        var isEligible = document.querySelector('input[name="eligibility"]:checked')?.value === 'Yes';

        submitButton.disabled = !(consentGiven && isEligible);
    }

    // Adding event listeners to the radio buttons
    consentRadios.forEach(function(radio) {
        radio.addEventListener('change', updateButtonState);
    });

    eligibilityRadios.forEach(function(radio) {
        radio.addEventListener('change', updateButtonState);
    });

    // Initial check in case the form is pre-filled or cached
    updateButtonState();


    // Handling form submission
    surveyForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Redirect to survey_id_entry.html
        window.location.href = '/survey_id_entry';
    });
});
