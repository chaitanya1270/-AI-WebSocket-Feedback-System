import pytest
import websockets
import asyncio
from server.server import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_quiz():
    # Test WebSocket connection and quiz functionality
    uri = "ws://localhost:8000/ws"  # Update the WebSocket URI as per your app

    async with websockets.connect(uri) as websocket:
        # Check welcome message
        welcome_message = await websocket.recv()
        assert "Welcome to the AI Quiz!" in welcome_message

        user_score = 0
        question_index = 0

        while True:
            try:
                # Receive a question from the server
                question = await websocket.recv()
                if "No more questions available" in question:
                    break

                # Send a response to the question
                await websocket.send("This is a sample response")

                # Receive feedback from the server
                feedback = await websocket.recv()
                assert feedback.startswith(("Excellent!", "Great!", "Good effort!", "Keep trying!", "Not quite right.", "Incorrect."))

                # Receive current score
                score_message = await websocket.recv()
                assert "Your current score" in score_message

                # Send "yes" to move to the next question
                await websocket.send("yes")

                question_index += 1
            except websockets.exceptions.ConnectionClosed:
                break

        # Receive the final score
        final_score_message = await websocket.recv()
        assert "Your final score is" in final_score_message

@pytest.mark.asyncio
async def test_home_page():
    # Test the home page HTML response
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
