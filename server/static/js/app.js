const websocket = new WebSocket("ws://localhost:8000/ws");
let count = 0;

websocket.onopen = () => {
    document.getElementById("message").innerText = "Connected to server.";
};

websocket.onmessage = (event) => {
    const message = event.data;

    if (message.startsWith("Question")) {
        // Display the new question
        document.getElementById("question").innerText = message;
        document.getElementById("feedback").innerText = "";
        document.getElementById("comment").innerText = "";
        document.getElementById("response").value = ""; // Clear input field
        document.getElementById("response").disabled = false; // Enable input field
        document.getElementById("response").style.visibility = "visible"; // Ensure it's visible
        toggleButtons("submit"); // Show only Submit button
        document.getElementById("message").innerText = "Please answer the question.";
    } else if (
        message.startsWith("Excellent") || 
        message.startsWith("Great") || 
        message.startsWith("Good effort") || 
        message.startsWith("Keep trying") || 
        message.startsWith("Incorrect")
    ) {
        // Display feedback for the current question
        document.getElementById("comment").innerText = message;
        document.getElementById("response").style.visibility = "hidden"; // Hide the response box after feedback
        toggleButtons("next"); // Show Next and End buttons after feedback
    } else if (message.startsWith("Your current score:")) {
        // Update the score on the frontend
        document.getElementById("score").innerText = message;
        count += 1;

        // Do nothing here, as we don't want to automatically show the next question
    } else {
        // Display general messages (e.g., welcome, end messages)
        document.getElementById("message").innerText = message;
        if (message.includes("Quiz ended")) {
            toggleButtons("none");
        }
    }
};

websocket.onclose = () => {
    document.getElementById("message").innerText = "Disconnected from server.";
};

// Button event listeners
document.getElementById("submit-btn").onclick = () => {
    const response = document.getElementById("response").value.trim();
    if (response) {
        console.log(response);
        websocket.send(response);
        document.getElementById("response").value = ""; // Clear input field after submission
        document.getElementById("response").disabled = true; // Disable input field after submission
        // Show only feedback (and hide input box)
        toggleButtons("none"); // Hide submit button after submission
    } else {
        document.getElementById("feedback").innerText = "Please enter a response.";
    }
};

document.getElementById("next-btn").onclick = () => {
    // Send message to move to the next question only when 'Next' is clicked.
    console.log("Moving to next question...");
    websocket.send("yes"); // Send 'yes' only when Next is clicked
    document.getElementById("response").disabled = false; // Enable input field for the next question
    document.getElementById("response").style.visibility = "visible"; // Ensure input box is visible again
    document.getElementById("response").value = ""; // Clear input field
    toggleButtons("submit"); // Show Submit button for the next question

    // Reset feedback and message
    document.getElementById("feedback").innerText = "";
    document.getElementById("message").innerText = "Please answer the next question.";
};

document.getElementById("end-btn").onclick = () => {
    // Send the "no" message to indicate the end of the quiz
    websocket.send("no");
    
    // Update the message to show "Quiz ended" and "Thank you for visiting"
    document.getElementById("message").innerText = "Quiz ended. Thank you for visiting.";
    
    // Hide all buttons since the quiz has ended
    toggleButtons("none");
};


// Utility to toggle button visibility
function toggleButtons(visibleButton) {
    const submitBtn = document.getElementById("submit-btn");
    const nextBtn = document.getElementById("next-btn");
    const endBtn = document.getElementById("end-btn");

    if (visibleButton === "submit") {
        submitBtn.style.display = "block";
        nextBtn.style.display = "none";
        endBtn.style.display = "none";
    } else if (visibleButton === "next") {
        submitBtn.style.display = "none";
        nextBtn.style.display = "block";
        endBtn.style.display = "block";
    } else {
        submitBtn.style.display = "none";
        nextBtn.style.display = "none";
        endBtn.style.display = "none";
    }
}
