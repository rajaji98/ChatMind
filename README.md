🧠 ChatMind --- Intelligent Group Chat Search

Search thousands of messy group-chat messages using natural language
--- even when the words in the query don't exactly match the original
message.

ChatMind is a semantic search system built for the "Search a Group
Chat Properly" vibe-coding challenge. It indexes a synthetic group
conversation and retrieves the most relevant messages using multilingual
sentence embeddings, semantic similarity, and intent-aware reranking.

✨ What It Does

ChatMind lets you ask questions like:

"When did everyone finally agree on our vacation?"

"What project did the group eventually choose?"

"What subject was the group's slide deck ultimately secured
around?"

Instead of relying only on keyword matching, ChatMind understands the
meaning of the query and retrieves relevant messages from the
conversation.

It also shows surrounding messages so the user can understand the full
conversation context behind a result.

🎯 Challenge Requirements

The dataset and search system were designed around the challenge
requirements:

4,000+ synthetic messages

8 participants

6 months of conversation

Messy Hinglish

Typos and informal language

Media / forwarded-message placeholders

3 decision threads

40 evaluation queries

8 hard queries with zero word overlap

Semantic/person/time-oriented search

Conversation context around retrieved messages

Top-1 and Top-5 evaluation

Dataset

Property                             Value

Messages                         4,569
Participants                         8
Time span                     6 months
Decision threads                     3
Evaluation queries                  40
Hard zero-overlap queries            8

🧠 How ChatMind Works

                 User Query
                     │
                     ▼
             ┌─────────────────┐
             │  Intent Detect  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Sentence        │
             │ Transformer     │
             │ Embeddings      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Semantic        │
             │ Similarity      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Intent-aware    │
             │ Reranking       │
             └────────┬────────┘
                      │
                      ▼
             Top Relevant Messages
                      │
                      ▼
             Conversation Context

Search pipeline

The user enters a natural-language query.

The Python search engine detects useful query intent such as:

final decision

who

when

where

alternatives

confirmation

The query is converted into a 384-dimensional multilingual
sentence embedding.

Candidate messages are ranked using semantic similarity.

Intent-aware reranking improves results for decision-oriented
questions.

The system returns the most relevant messages along with nearby
conversation context.

Embedding model

ChatMind uses:

sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

This makes it suitable for the dataset's mixed-language / Hinglish
conversation style.

🔎 Example: Semantic Search

Query

"When did everyone finally agree on our vacation?"

The query does not need to exactly contain the words from the original
decision.

ChatMind retrieves:

Priya: Guys Manali fix hai 🏔️

with surrounding context:

Ankit   same
Rahul   toh destination final kar dein?
Priya   Guys Manali fix hai 🏔️
Aman    done, tickets dekhte hain
Rohit   finally trip locked 😂

This demonstrates semantic retrieval rather than simple exact keyword
matching.

📊 Evaluation

The system was evaluated on 40 queries:

32 normal queries

8 hard queries with zero lexical overlap

Current results

Metric                          Score

Overall Top-1               85.0%
Normal Top-1                84.4%
Hard Top-1                  87.5%
Overall Top-5               97.5%
Hard zero-overlap check      PASS

The evaluation uses the project's predefined target message IDs and
reports actual retrieval performance.

🧪 Three Decision Threads

The synthetic dataset contains three intentionally structured decision
conversations.

🏔️ Travel

The group discusses options and eventually decides on Manali.

💻 Project

The group considers several project ideas and finally selects a
student productivity dashboard.

🌱 Presentation

The group organizes a presentation and locks the topic as renewable
energy.

These threads provide realistic multi-message decision chains for
testing semantic retrieval and conversation context.

🛠️ Tech Stack

Frontend

HTML

CSS

Vanilla JavaScript

Backend

Node.js

Express

CORS

Search / AI

Python

NumPy

Sentence Transformers

paraphrase-multilingual-MiniLM-L12-v2

📁 Project Structure

chatmind/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── backend/
│   ├── server.js
│   └── data/
│       ├── messages.json
│       └── evaluations.json
│
├── scripts/
│   ├── search_engine.py
│   ├── generate_chat.py
│   ├── generate_embeddings.py
│   └── evaluate.py
│
├── embeddings/
├── requirements.txt
├── package.json
├── .gitignore
└── README.md

🚀 Run Locally

1. Clone the repository

git clone https://github.com/rajaji98/ChatMind

cd chatMind

2. Install Node dependencies

npm install

3. Create and activate a Python virtual environment

Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

4. Install Python dependencies

pip install -r requirements.txt

5. Start the server

node .\backend\server.js

The application will be available at:

http://localhost:5000

Open that address in your browser.

🔬 Run the Search Engine Directly

You can also test the Python search engine without the frontend:

python scripts/search_engine.py "What project did the group eventually choose?" --json

📈 Run Evaluation

python scripts/evaluate.py

This evaluates the predefined 40-query test set and reports Top-1 /
Top-5 retrieval performance.

💡 Example Queries

Try these in the UI:

When did everyone finally agree on our vacation?

What project did the group eventually choose?

What subject was the group's slide deck ultimately secured around?

Which idea survived all the alternatives and became the group's selected build?

Where did the friends eventually settle for their getaway?

🎨 Interface

ChatMind provides:

Dark modern interface

Natural-language search

Relevance scores

Sender information

Timestamp

Decision / agreement labels

Thread information

Conversation context

Example search queries

Responsive layout

🔐 Data

The dataset is synthetic and was created specifically for evaluating
the search system. It does not represent a real private group
conversation.

🎯 Why ChatMind?

Traditional chat search often depends heavily on exact words.

Someone may ask:

"When did everyone finally agree on our vacation?"

while the actual message says:

"Guys Manali fix hai 🏔️"

ChatMind is designed to bridge that gap by combining semantic
understanding + intent-aware ranking + conversation context.

👨‍💻 Built For

ITGeeks Vibe Coding Round --- "Search a Group Chat Properly"

Built as a focused semantic retrieval system rather than a generic
chatbot.