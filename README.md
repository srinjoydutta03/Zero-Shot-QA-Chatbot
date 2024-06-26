# Zero-Shot-QA Chatbot

## Overview

Zero-Shot-QA Chatbot is an intelligent conversational agent designed to provide accurate answers and information without the need for prior training on specific datasets. The chatbot leverages advanced AI models, including OpenAI's GPT, Vertex AI for embeddings, and web search capabilities, to understand and respond to user queries effectively. It utilizes a combination of Tree of Thoughts prompting and Retrieval-Augmented Generation (RAG) to generate high-quality answers. The chatbot also makes intelligent decisions on whether to perform a search API call based on similarity search results.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Frontend Interface](#frontend-interface)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Zero-Shot Learning**: The chatbot can answer questions without needing domain-specific training.
- **Vertex AI Integration**: Utilizes Google Cloud’s Vertex AI for embeddings and document storage.
- **Web Research Capabilities**: Integrates Google Search API for real-time information retrieval.
- **Tree of Thoughts Prompting**: Enhances the reasoning process by simulating multiple experts brainstorming.
- **Retrieval-Augmented Generation (RAG)**: Combines document retrieval and generation to produce high-quality responses.
- **FastAPI Backend**: Provides a robust and scalable backend API.
- **React Frontend**: A user-friendly interface for interacting with the chatbot.
- **Redis Integration**: Stores conversations for session continuity.

## Architecture

The architecture of the Zero-Shot-QA Chatbot includes the following components:

1. **Frontend**: A React application that provides the user interface.
2. **Backend**: FastAPI server that handles user queries and integrates with various AI and web search services.
3. **Redis**: Used for session management and storing conversation history.
4. **Vertex AI**: Provides embeddings and vector search capabilities for document retrieval.

## Installation

### Prerequisites

- Node.js and npm
- Python 3.8+
- Redis server
- Google Cloud account with Vertex AI enabled
- OpenAI API key

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/zero-shot-qa-chatbot.git
   cd zero-shot-qa-chatbot
   ```

2. **Backend Setup:**

   - Navigate to the backend directory:
     ```bash
     cd chatbot-backend
     ```

   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

   - Set up environment variables:
     Create a `.env` file and add the following:
     ```
     OPENAI_API_KEY = your_openai_api_key
     GOOGLE_CSE_ID = your_google_custom_search_engine_id
     GOOGLE_API_KEY = your_google_api_key
     PROJECT_ID = your_gcp_project_id
     REGION = your_gcp_region
     BUCKET_NAME = your_gcs_bucket
     INDEX_ID = your_index_id
     INDEX_ENDPOINT_ID = your_index_endpoint_id
     ```

   - Start the FastAPI server:
     ```bash
     uvicorn src.conversation_service:app --reload
     ```

3. **Frontend Setup:**

   - Navigate to the frontend directory:
     ```bash
     cd chatbot-frontend
     ```

   - Install the dependencies:
     ```bash
     npm install
     ```

   - Start the React development server:
     ```bash
     npm run dev
     ```

## Usage

1. **Starting the Services:**
   Ensure Redis server is running. Start both the backend and frontend servers as described in the installation steps.

2. **Interacting with the Chatbot:**
   Open your browser and go to `http://localhost:5173` to interact with the chatbot through the user-friendly interface.


## API Endpoints

### Backend Endpoints

- **GET /conversations/{conversation_id}**
  - Retrieves the conversation history for the given conversation ID.

- **POST /conversations/{conversation_id}**
  - Processes a new user message, fetches the AI response, and updates the conversation history.

### Frontend Components

- **App.js**: Main React component for the chatbot interface.
- **index.js**: Entry point for the React application.
- **index.css**: Contains the styles for the frontend.

## Screenshots

- ![Chat Interface](https://github.com/srinjoydutta03/Zero-Shot-QA-Chatbot/screenshots/landing_page.png)
- ![Loading Screen](https://github.com/srinjoydutta03/Zero-Shot-QA-Chatbot/screenshots/loading_page.png)
- ![Conversation History](https://github.com/srinjoydutta03/Zero-Shot-QA-Chatbot/screenshots/answers.png)
