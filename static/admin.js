const socket = io.connect();

document.getElementById("nextQuestion").addEventListener("click", () => {
  socket.emit("admin_next_question");
});

socket.on("new_question", (question) => {
  // Display the new question for players
  console.log("New Question:", question);
});
