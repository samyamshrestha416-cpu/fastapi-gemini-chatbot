# Chatbot API

A chatbot API built with **FastAPI**, **Google Gemini**, and **PostgreSQL**.
It remembers each conversation: every message is saved in the database, and the
full history is sent to the model with each new question.

This is a learning project. I built it to understand how LLM API calls work and
why a chatbot needs a database to "remember".

## How it works

The model itself has no memory. Each request to `POST /chat` does four things:

1. Loads the earlier messages of that conversation from PostgreSQL.
2. Sends the history plus the new message to Gemini.
3. Saves the user's message and the model's reply in the database.
4. Returns the reply.

Different `conversation_id` values are separate chats, each with its own history.

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Google Gemini API (`google-genai`)
- python-dotenv

## Project structure

```
chatbot_api/
├── main.py            # FastAPI app and the /chat route
├── llm.py             # Gemini call: builds the message list and gets the reply
├── services.py        # Database functions: save_message, get_history
├── models.py          # SQLAlchemy table for chat messages
├── db.py              # Database connection and session
├── requirements.txt   # Python packages
└── .gitignore         # Keeps .env and venv out of Git
```

## Setup

1. **Create a PostgreSQL database** named `chatbot`:

   ```sql
   CREATE DATABASE chatbot;
   ```

2. **Create a virtual environment and install the packages:**

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Get a Gemini API key** from Google AI Studio (it has a free tier).

4. **Create a `.env` file** in the project folder (never upload this file):

   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/chatbot
   GEMINI_API_KEY=your_key_here
   ```

   Use a password with only letters and numbers, so the URL does not break.

5. **Run the server:**

   ```bash
   python -m uvicorn main:app --reload
   ```

   The tables are created automatically when the app starts.

6. Open **http://127.0.0.1:8000/docs** to try the API.

## Example

**Request**: `POST /chat`

```json
{
  "conversation_id": 1,
  "message": "My name is Samyam."
}
```

**Response**

```json
{
  "reply": "Nice to meet you, Samyam!"
}
```

Then ask in the same conversation:

```json
{
  "conversation_id": 1,
  "message": "What is my name?"
}
```

The model answers with your name, because the earlier messages were loaded from
the database and sent along with the new one. Using a different
`conversation_id` starts a fresh chat with no memory.

## Error handling

| Status | Meaning |
|--------|---------|
| 422 | Invalid input, for example an empty message |
| 502 | The AI service failed (overloaded, wrong key, timeout). Try again. |

## What I learned

- Calling an LLM API with a system prompt
- Keeping secrets in a `.env` file
- Why the model needs the whole history on every call
- Storing and loading chat history with SQLAlchemy and PostgreSQL
- Handling API failures without crashing the app

## Ideas for improvement

- A `GET /chat/{conversation_id}` route to read a saved conversation
- A route to delete a conversation
- Limit the history to the last N messages
- Streaming replies
