# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from sentence_transformers import SentenceTransformer, util
# from collections import defaultdict
# import asyncio
# import random
# import logging
# from pathlib import Path

# app = FastAPI()

# # Load AI model for semantic similarity
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Set to manage connected clients and cache
# connected_clients = set()
# response_cache = defaultdict(dict)  # Caches user responses
# scores = defaultdict(int)  # Tracks user scores

# # Logging setup
# log_file = Path("logs/server.log")
# log_file.parent.mkdir(parents=True, exist_ok=True)
# logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# # AI-related questions and answers
# questions = [
    # {"question": "What is Artificial Intelligence?", 
    #  "answer": "Artificial intelligence is the simulation of human intelligence in machines."},
     
    # {"question": "What is Machine Learning?", 
    #  "answer": "Machine learning is a subset of AI that involves training machines to learn from data."},
     
    # {"question": "What is Deep Learning?", 
    #  "answer": "Deep learning is a subset of machine learning using neural networks to process large amounts of data."},
     
    # {"question": "What is Supervised Learning?", 
    #  "answer": "Supervised learning is a machine learning technique using labeled data to train algorithms."},
     
    # {"question": "What is Unsupervised Learning?", 
    #  "answer": "Unsupervised learning is a machine learning technique that works with unlabeled data to find hidden patterns."},
     
    # {"question": "What is Reinforcement Learning?", 
    #  "answer": "Reinforcement learning is a type of machine learning where an agent learns to make decisions by receiving rewards or penalties."},
     
    # {"question": "What is Natural Language Processing?", 
    #  "answer": "Natural language processing is a branch of AI that deals with the interaction between computers and humans using natural language."},
     
    # {"question": "What is a Neural Network?", 
    #  "answer": "A neural network is a computational model inspired by the human brain, used to recognize patterns and solve complex problems."},
     
    # {"question": "What is Computer Vision?", 
    #  "answer": "Computer vision is a field of AI that enables computers to interpret and process visual data like images and videos."},
     
    # {"question": "What is Data Preprocessing?", 
    #  "answer": "Data preprocessing involves cleaning and preparing raw data to make it suitable for machine learning models."},
     
    # {"question": "What is Overfitting?", 
    #  "answer": "Overfitting occurs when a machine learning model learns the training data too well and performs poorly on new data."},
     
    # {"question": "What is Underfitting?", 
    #  "answer": "Underfitting occurs when a machine learning model is too simple to capture the underlying patterns in the data."},
     
    # {"question": "What is Gradient Descent?", 
    #  "answer": "Data preprocessing involves cleaning and preparing raw data to make it suitable for machine learning models."},
     
    # {"question": "What is a Decision Tree?", 
    #  "answer": "A decision tree is a flowchart-like structure used for decision-making and predictive modeling in machine learning."},
     
    # {"question": "What is Clustering?", 
    #  "answer": "Clustering is an unsupervised learning technique that groups similar data points together based on features."},
     
    # {"question": "What is Transfer Learning?", 
    #  "answer": "Transfer learning involves using a pre-trained model on a new but related task to save time and resources."},
     
    # {"question": "What is Bias in Machine Learning?", 
    #  "answer": "Bias in machine learning refers to systematic errors introduced by incorrect assumptions in the learning algorithm."},
     
    # {"question": "What is Variance in Machine Learning?", 
    #  "answer": "Variance refers to the model's sensitivity to changes in the training data, often leading to overfitting."},
     
    # {"question": "What is the Turing Test?", 
    #  "answer": "The Turing Test is a method of determining whether a machine can exhibit human-like intelligence."},
     
    # {"question": "What is Big Data?", 
    #  "answer": "Big data refers to extremely large datasets that are difficult to process and analyze using traditional methods."},
     
    # {"question": "What is Feature Engineering?", 
    #  "answer": "Feature engineering is the process of selecting and transforming data features to improve model performance."},
     
    # {"question": "What is an Activation Function?", 
    #  "answer": "An activation function determines the output of a neural network layer and introduces non-linearity into the model."},
     
    # {"question": "What is Hyperparameter Tuning?", 
    #  "answer": "Hyperparameter tuning involves optimizing the configuration of a machine learning model to improve its performance."},
     
    # {"question": "What is a Support Vector Machine (SVM)?", 
    #  "answer": "A support vector machine is a supervised learning algorithm used for classification and regression tasks."},
     
    # {"question": "What is the difference between AI, ML, and DL?", 
    #  "answer": "AI is a broad concept of creating intelligent machines, ML is a subset of AI focused on learning from data, and DL is a subset of ML using neural networks."}
# ]

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     connected_clients.add(websocket)
#     logging.info("New client connected")

#     score = 0  # Initialize score
#     attempted = 0  # Track number of questions attempted
#     random.shuffle(questions)  # Randomize questions

#     try:
#         await websocket.send_text("Welcome to the AI Quiz! Answer the questions as best as you can. Type 'exit' at any time to quit.")

#         for i, qa in enumerate(questions, start=1):
#             question, correct_answer = qa["question"], qa["answer"]

#             # Send question
#             await websocket.send_text(f"Question {i}: {question}")

#             while True:  # Loop for user response to current question
#                 try:
#                     response = await asyncio.wait_for(websocket.receive_text(), timeout=60)
#                     logging.info(f"Received response: {response}")

#                     if response.lower() == "exit":
#                         await websocket.send_text("Exiting the quiz. Thank you for participating!")
#                         await websocket.close()
#                         return

#                     if question in response_cache[websocket]:
#                         await websocket.send_text("You've already answered this question.")
#                         break

#                     response_cache[websocket][question] = response
#                     attempted += 1

#                     # Analyze response
#                     similarity = analyze_response(response, correct_answer)

#                     # Feedback and scoring
#                     if similarity > 0.90:
#                         feedback = "Excellent! You nailed it! 😁"
#                         score += 5
#                     elif 0.80 < similarity <= 0.90:
#                         feedback = "Great! You're very close. 🙂"
#                         score += 4
#                     elif 0.70 < similarity <= 0.80:
#                         feedback = "Good effort! Almost there. 🤨"
#                         score += 3
#                     elif 0.50 < similarity <= 0.70:
#                         feedback = "Keep trying! You can do it! 😐"
#                         score += 2
#                     elif 0.30 < similarity <= 0.50:
#                         feedback = "Not quite right. Review and try again. 😓"
#                         score += 1
#                     else:
#                         feedback = "Incorrect. Don't give up! ❌"

#                     # Send feedback and updated score
#                     await websocket.send_text(f"Feedback: {feedback}")
#                     await websocket.send_text(f"Your Current Score: {score}/{attempted * 5}")

#                     # Ask to continue directly
#                     await websocket.send_text("Do you want to proceed to the next question? (yes/exit)")
#                     next_step = await asyncio.wait_for(websocket.receive_text(), timeout=60)

#                     if next_step.lower() == "yes":
#                         break
#                     elif next_step.lower() == "exit":
#                         await websocket.send_text(f"Exiting the quiz. Thank you for participating!\nQuiz completed!\nYou attempted {attempted} questions.\nYour final score is {score}/{attempted * 5}.")
                        
#                         await websocket.close()
#                         return
#                     else:
#                         await websocket.send_text("Invalid input. Please type 'yes' or 'exit'.")

#                 except asyncio.TimeoutError:
#                     await websocket.send_text("Timeout: Moving to the next question.")
#                     break

#         # Quiz completion message

#     except WebSocketDisconnect:
#         logging.info("Client disconnected")
#     finally:
#         connected_clients.remove(websocket)

# def analyze_response(response: str, correct_answer: str) -> float:
#     """Analyze response similarity to the correct answer."""
#     response_vec = model.encode(response, convert_to_tensor=True)
#     answer_vec = model.encode(correct_answer, convert_to_tensor=True)
#     similarity = util.cos_sim(response_vec, answer_vec).item()
#     return similarity

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer, util
import logging
import asyncio
import random
from pathlib import Path

app = FastAPI()

# Static and templates setup
app.mount("/static", StaticFiles(directory="server/static"), name="static")
templates = Jinja2Templates(directory="server/Templates")

# Model setup
model = SentenceTransformer("all-MiniLM-L6-v2")

# Logging setup
log_file = Path("logs/server.log")
log_file.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Questions and answers
questions = [
    {"question": "What is Artificial Intelligence?", 
     "answer": "Artificial intelligence is the simulation of human intelligence in machines."},
     
    {"question": "What is Machine Learning?", 
     "answer": "Machine learning is a subset of AI that involves training machines to learn from data."},
     
    {"question": "What is Deep Learning?", 
     "answer": "Deep learning is a subset of machine learning using neural networks to process large amounts of data."},
     
    {"question": "What is Supervised Learning?", 
     "answer": "Supervised learning is a machine learning technique using labeled data to train algorithms."},
     
    {"question": "What is Unsupervised Learning?", 
     "answer": "Unsupervised learning is a machine learning technique that works with unlabeled data to find hidden patterns."},
     
    {"question": "What is Reinforcement Learning?", 
     "answer": "Reinforcement learning is a type of machine learning where an agent learns to make decisions by receiving rewards or penalties."},
     
    {"question": "What is Natural Language Processing?", 
     "answer": "Natural language processing is a branch of AI that deals with the interaction between computers and humans using natural language."},
     
    {"question": "What is a Neural Network?", 
     "answer": "A neural network is a computational model inspired by the human brain, used to recognize patterns and solve complex problems."},
     
    {"question": "What is Computer Vision?", 
     "answer": "Computer vision is a field of AI that enables computers to interpret and process visual data like images and videos."},
     
    {"question": "What is Data Preprocessing?", 
     "answer": "Data preprocessing involves cleaning and preparing raw data to make it suitable for machine learning models."},
     
    {"question": "What is Overfitting?", 
     "answer": "Overfitting occurs when a machine learning model learns the training data too well and performs poorly on new data."},
     
    {"question": "What is Underfitting?", 
     "answer": "Underfitting occurs when a machine learning model is too simple to capture the underlying patterns in the data."},
     
    {"question": "What is Gradient Descent?", 
     "answer": "Gradient descent is an optimization algorithm used to minimize a function, commonly used in machine learning models."},
     
    {"question": "What is a Decision Tree?", 
     "answer": "A decision tree is a flowchart-like structure used for decision-making and predictive modeling in machine learning."},
     
    {"question": "What is Clustering?", 
     "answer": "Clustering is an unsupervised learning technique that groups similar data points together based on features."},
     
    {"question": "What is Transfer Learning?", 
     "answer": "Transfer learning involves using a pre-trained model on a new but related task to save time and resources."},
     
    {"question": "What is Bias in Machine Learning?", 
     "answer": "Bias in machine learning refers to systematic errors introduced by incorrect assumptions in the learning algorithm."},
     
    {"question": "What is Variance in Machine Learning?", 
     "answer": "Variance refers to the model's sensitivity to changes in the training data, often leading to overfitting."},
     
    {"question": "What is the Turing Test?", 
     "answer": "The Turing Test is a method of determining whether a machine can exhibit human-like intelligence."},
     
    {"question": "What is Big Data?", 
     "answer": "Big data refers to extremely large datasets that are difficult to process and analyze using traditional methods."},
     
    {"question": "What is Feature Engineering?", 
     "answer": "Feature engineering is the process of selecting and transforming data features to improve model performance."},
     
    {"question": "What is an Activation Function?", 
     "answer": "An activation function determines the output of a neural network layer and introduces non-linearity into the model."},
     
    {"question": "What is Hyperparameter Tuning?", 
     "answer": "Hyperparameter tuning involves optimizing the configuration of a machine learning model to improve its performance."},
     
    {"question": "What is a Support Vector Machine (SVM)?", 
     "answer": "A support vector machine is a supervised learning algorithm used for classification and regression tasks."},
     
    {"question": "What is the difference between AI, ML, and DL?", 
     "answer": "AI is a broad concept of creating intelligent machines, ML is a subset of AI focused on learning from data, and DL is a subset of ML using neural networks."}
]

connected_clients = set()


@app.get("/", response_class=HTMLResponse)
async def home():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    user_score = 0  # To keep track of the user's score
    question_index = 0  # To track the question number

    try:
        await websocket.send_text("Welcome to the AI Quiz! Answer the following questions.")
        random.shuffle(questions)

        while True:
            if question_index >= len(questions):
                await websocket.send_text("No more questions available. Ending the quiz.")
                break

            # Ask the current question
            current_question = questions[question_index]
            question, correct_answer = current_question["question"], current_question["answer"]
            question_index += 1

            await websocket.send_text(f"Question {question_index}: {question}")

            # Wait for a response from the client before continuing
            response = await websocket.receive_text()
            similarity = util.cos_sim(
                model.encode(response, convert_to_tensor=True),
                model.encode(correct_answer, convert_to_tensor=True)
            ).item()

            # Feedback and scoring based on similarity
            if similarity > 0.90:
                feedback = "Excellent! You nailed it! 😁"
                user_score += 5
            elif 0.80 < similarity <= 0.90:
                feedback = "Great! You're very close. 🙂"
                user_score += 4
            elif 0.70 < similarity <= 0.80:
                feedback = "Good effort! Almost there. 🤨"
                user_score += 3
            elif 0.50 < similarity <= 0.70:
                feedback = "Keep trying! You can do it! 😐"
                user_score += 2
            elif 0.30 < similarity <= 0.50:
                feedback = "Not quite right. Review and try again. 😓"
                user_score += 1
            else:
                feedback = "Incorrect. Don't give up! ❌"

            # Send feedback and current score
            await websocket.send_text(feedback)
            await websocket.send_text(f"Your current score: {user_score}")

            # Wait for the "Next" button click before moving to the next question
            move_to_next = await websocket.receive_text()  # This will be "yes" when Next is clicked
            if move_to_next.lower() == "yes":
                continue

        await websocket.send_text(f"Thanks for participating in the quiz! Your final score is {user_score}.")

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logging.info("Client disconnected")
