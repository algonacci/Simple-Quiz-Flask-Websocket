const socket = io.connect();
let currentQuestion = null;

const playerName = prompt("Enter your name:");
socket.emit("player_join", playerName);

socket.on("update_players", (players) => {
  // Update the player list UI
  console.log("Players:", players);
});

socket.on("new_question", (question) => {
  // Display the new question and options for players
  console.log("New Question:", question);
  currentQuestion = question;
  displayQuestion(question);
});

socket.on("quiz_completed", () => {
  // Display game over message when the quiz is completed
  console.log("Quiz completed!");
  displayGameOver();
});

function submitAnswer(selected_option) {
  if (currentQuestion) {
    socket.emit("player_answer", { selected_option });
  }
}

socket.on("answer_feedback", (feedback) => {
  // Display whether the answer is correct or not
  console.log("Answer Feedback:", feedback);
  displayAnswerFeedback(feedback);
});

function displayQuestion(question) {
  // Display the question and options in the UI
  const questionContainer = document.getElementById("questionContainer");
  questionContainer.innerHTML = `
        <h2>${question.question}</h2>
        <ul>
            ${question.options
              .map(
                (option) => `
                <li>
                    <button onclick="submitAnswer('${option}')">${option}</button>
                </li>
            `
              )
              .join("")}
        </ul>
    `;
}

function displayAnswerFeedback(feedback) {
  // Display feedback about the answer (correct or incorrect)
  const questionContainer = document.getElementById("questionContainer");
  questionContainer.innerHTML += `
        <p>${feedback.is_correct ? "Correct!" : "Incorrect!"}</p>
    `;
}

function displayGameOver() {
  // Display a game over message in the UI
  const questionContainer = document.getElementById("questionContainer");
  questionContainer.innerHTML = `
        <h2>Quiz Completed</h2>
        <p>Thank you for playing!</p>
    `;
}
