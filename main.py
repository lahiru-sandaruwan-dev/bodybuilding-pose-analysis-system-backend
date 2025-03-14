 
# main.py

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8080)

from app import create_app
from flask_socketio import SocketIO

# Create app instance
app = create_app()

# Initialize SocketIO
socketio = SocketIO(app)

if __name__ == "__main__":
    # Run the app with SocketIO
    socketio.run(app, debug=True, port=8080)

# from app import create_app
# from flask_socketio import SocketIO
# from flask_cors import CORS

# # Create Flask app
# app = create_app()

# # Enable CORS for all routes (including Socket.IO requests)
# CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# # Initialize SocketIO with explicit CORS settings and WebSocket transport
# socketio = SocketIO(
#     app,
#     cors_allowed_origins="http://localhost:4200",  # Allow requests from Angular
#     transports=["websocket", "polling"]  # Allow both WebSocket and polling
# )

# # SocketIO event handling (add your events here)
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")

# # Run the app with WebSocket support
# if __name__ == "__main__":
#     socketio.run(app, debug=True, host="127.0.0.1", port=8080)





