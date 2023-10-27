// script.js

// Save answer when user navigates to the next question
function saveAnswer(questionNumber, answer) {
	// console.log('Saved answer ' + answer + ' for question ' + questionNumber);
	// localStorage.setItem('answer_' + questionNumber, answer);
}

// Load answer when user navigates to a question
function loadAnswer(questionNumber) {
    // console.log('Loaded answer ' + localStorage.getItem('answer_' + questionNumber) + ' for question ' + questionNumber);
	// return localStorage.getItem('answer_' + questionNumber);
}

// Function to get the current question number (you'll need to implement this)
function getCurrentQuestionNumber() {
    // let path = window.location.pathname;
    // let match = path.match(/question_(\d+)\.html/);
    // return match ? parseInt(match[1], 10) : null;
}

function submitResponses() {
    // console.log("Submitting responses");
	
	// let answerField = document.querySelector('#answer') || document.querySelector('input[name="answer"]:checked') || document.querySelector('input[name="rating"]:checked');
    // if (answerField) {
    //     saveAnswer(currentQuestionNumber, answerField.value);
    // }
			
    // // Collect responses from localStorage
    // let responses = {};
    // for (let i = 0; i < localStorage.length; i++) {
    //     let key = localStorage.key(i);
    //     if (key.startsWith('answer_')) {
    //         responses[key] = localStorage.getItem(key);
    //     }
    // }

    // // Send responses to server
    // fetch('/submit', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify(responses)
    // })
    //     .then(response => response.text())
    //     .then(data => {
    //         console.log(data);  // Log server response
    //         // Optionally, clear responses from localStorage
    //         localStorage.clear();
    //     });
}

// Event listener to save and load answers on button clicks
document.addEventListener('DOMContentLoaded', (event) => {
	let form = document.getElementById('question-form');  // Assuming the form has an id of 'question-form'
	console.log(typeof form.action);  // log the type of form.action
	console.log(form.action.toString());  // try converting form.action to a string
    // let nextButton = document.querySelector('#next-button');
    // let backButton = document.querySelector('#back-button');
	// let submitButton = document.querySelector('.submit-button');
    // let currentQuestionNumber = getCurrentQuestionNumber();
    
    // if (nextButton) {
    //     console.log('nextButton')
    //     nextButton.addEventListener('click', () => {
    //         let answerField = document.querySelector('#answer') || document.querySelector('input[name="answer"]:checked') || document.querySelector('input[name="rating"]:checked');
    //         if (answerField) {
    //             saveAnswer(currentQuestionNumber, answerField.value);
    //         }
    //     });
    // }
    // else{
    //     console.log('nextButton not found')
    // }
	
	
    // if (backButton) {
    //     console.log('backButton')
    //     backButton.addEventListener('click', () => {
    //         let answerField = document.querySelector('#answer') || document.querySelector('input[name="answer"]:checked') || document.querySelector('input[name="rating"]:checked');
    //         if (answerField) {
    //             saveAnswer(currentQuestionNumber, answerField.value);
    //         }
    //     });
    // }
    // else{
    //     console.log('backButton not found')
    // }
	
	// if(submitButton) {
    //     submitButton.addEventListener('click', submitResponses);
    // }
    // else{
    //     console.log('submitButton not found')
    // }

    // // Load answer when the page loads
    // let answer = loadAnswer(currentQuestionNumber);
    // if (answer !== null) {
    //     let answerField = document.querySelector('#answer');
    //     if (answerField) {
    //         answerField.value = answer;
    //     } else {
    //         let radioBtn = document.querySelector(`input[name="answer"][value="${answer}"]`) || document.querySelector(`input[name="rating"][value="${answer}"]`);
    //         if (radioBtn) {
    //             radioBtn.checked = true;
    //         }
    //     }
    // }
});
