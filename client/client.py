# import asyncio
# import websockets
# from websockets.exceptions import ConnectionClosed, ConnectionClosedError

# async def websocket_client():
#     uri = "ws://localhost:8000/ws"
#     try:
#         async with websockets.connect(uri, ping_interval=30, ping_timeout=30) as websocket:
#             print("Connected to the WebSocket server.")

#             try:
#                 welcome_message = await websocket.recv()
#                 print(f"Server: {welcome_message}")  # Welcome message

#                 while True:
#                     try:
#                         # Wait for a message from the server
#                         message = await asyncio.wait_for(websocket.recv(), timeout=60)
#                         print(f"Server: {message}")

#                         # Handle server messages
#                         if "Your Current Score" in message:
#                             print("Server shared your current score.")
#                             continue
#                         elif "Do you want to proceed" in message:
#                             response = input("Your choice (yes/exit): ")
#                             await websocket.send(response)
#                         elif "Thank you for participating" in message:
#                             print("Quiz ended. Exiting.")
#                             break
#                         elif "Question" in message:
#                             response = input("Your response: ")
#                             await websocket.send(response)
#                         else:
#                             print("Unhandled server message.")
#                             continue

#                     except asyncio.TimeoutError:
#                         print("Timeout: No response from server within 60 seconds. Closing connection.")
#                         break
#                     except ConnectionClosedError as e:
#                         print(f"Connection closed unexpectedly: {e}")
#                         break

#             except Exception as e:
#                 print(f"An error occurred during communication: {e}")

#     except ConnectionClosed as e:
#         print(f"Connection closed during setup: {e}")
#     except Exception as e:
#         print(f"Failed to connect to the WebSocket server: {e}")

# if __name__ == "__main__":
#     print("Starting WebSocket client...")
#     asyncio.run(websocket_client())

import asyncio
import websockets

async def websocket_client():
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the server.")
            
            # Infinite loop to handle messages and send responses
            while True:
                try:
                    # Receive a message from the server
                    message = await websocket.recv()
                    print(f"Server: {message}")

                    # Handle questions or other types of messages
                    if message.startswith("Question"):
                        response = None
                        
                        # Loop until a valid response is entered
                        while not response:
                            response = input("Your answer: ").strip()
                            if not response:
                                print("Response cannot be empty. Please try again.")

                        # Send the response back to the server
                        await websocket.send(response)

                except websockets.ConnectionClosed:
                    print("Connection closed by the server.")
                    break

    except ConnectionRefusedError:
        print("Could not connect to the server. Ensure the server is running and try again.")

# Run the client
if __name__ == "__main__":
    asyncio.run(websocket_client())
