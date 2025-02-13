# Audio Transcriber with AI

A simple REST API that transcribes audio files using AI-powered Speech-to-Text technology.

## Installation

### 1. Set Up Environment Variables
Create a `.env` file in the project root and add your GROQ API key from here https://console.groq.com/playground:
```
GROQ_API_KEY=your_api_key_here
```

### 2. Install Dependencies
Run the following commands in the project folder:
```sh
py -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the Server
Run the following command to start the FastAPI server:
```sh
uvicorn main:app --reload
```

## Project Structure
```
project-folder/
│── main.py               # Main FastAPI application
│── .env                  # API keys and environment variables
│── uploads/              # Directory for storing audio files
│── requirements.txt       # Python dependencies
```
