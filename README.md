<div align="center">

🧠 ChatMind — Intelligent Group Chat Search

Search thousands of messy group-chat messages with natural language

Semantic search • Intent-aware reranking • Conversation context

<br>






</div>

📌 Overview

ChatMind is a semantic group-chat search engine built for the ITGeeks "Search a Group Chat Properly" vibe-coding challenge.

Instead of depending only on exact keywords, ChatMind converts natural-language queries and chat messages into multilingual sentence embeddings, ranks candidate messages by semantic similarity, and then applies intent-aware reranking to surface better answers.

The result is a search experience that can connect very different wording to the same underlying meaning.

Example

Query: "When did everyone finally agree on our vacation?"

Retrieved message: "Guys Manali fix hai 🏔️"

The wording is different, but the meaning is closely related.

✨ What It Does

ChatMind allows users to search a large, messy group conversation using natural language.

🔎 Natural-Language Search

Ask questions the way you would ask a friend:

"When did everyone finally agree on our vacation?"

"What project did the group eventually choose?"

"What subject was the group's slide deck ultimately secured around?"

🧠 Semantic Understanding

The system does not rely only on exact word overlap. It uses multilingual sentence embeddings to retrieve messages with similar meaning.

🎯 Intent-Aware Ranking

Queries can contain useful intent such as:

final decision

who

when

where

alternatives

confirmation

That intent is used during reranking to improve decision-oriented searches.

💬 Conversation Context

Every retrieved result includes nearby messages so the user can see the discussion that led to the answer.

🏷️ Useful Message Metadata

Results show:

sender

timestamp

relevance score

thread

message type

conversation context

🎯 Challenge Coverage

The project was designed around the challenge requirements.

Requirement

Implementation

4,000+ messages

4,569 synthetic messages

8 participants

✅

6 months

✅

Messy Hinglish

✅

Typos / informal language

✅

Media / forwarded lines

✅

3 decision threads

✅

40 evaluation queries

✅

8 hard zero-overlap queries

✅

Semantic search

✅

Person / time-oriented intent

✅

Conversation context

✅

Top-1 / Top-5 evaluation

✅

📊 Dataset

The included synthetic dataset contains realistic-style chat noise and structured decision conversations.

Property

Value

💬 Messages

4,569

👥 Participants

8

📅 Time span

6 months

🧵 Decision threads

3

🧪 Evaluation queries

40

🔥 Hard zero-overlap queries

8

Participants

The group contains eight synthetic participants:

Aman · Priya · Rahul · Neha · Rohit · Sneha · Karan · Ankit

🧠 How ChatMind Works

                         User Query
                              │
                              ▼
                    ┌──────────────────┐
                    │   Intent Detect   │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Sentence         │
                    │ Transformer      │
                    │ Embeddings       │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Semantic         │
                    │ Similarity       │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Intent-aware     │
                    │ Reranking        │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Top Relevant     │
                    │ Messages         │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Conversation     │
                    │ Context          │
                    └──────────────────┘

🔄 Search Pipeline

1. Query

The user enters a natural-language question.

2. Intent Detection

The search engine looks for signals such as final decisions, people, time, location, alternatives, and confirmation.

3. Embedding

The query is converted into a 384-dimensional multilingual sentence embedding.

4. Semantic Retrieval

Messages are ranked by semantic similarity to the query.

5. Intent-Aware Reranking

Additional signals are used to promote messages that better match the user's question intent.

6. Context Retrieval

Nearby messages are returned with the winning result so the user can understand the conversation.

🤖 Embedding Model

ChatMind uses:

sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

The model produces 384-dimensional embeddings and is used here because the dataset contains mixed-language / Hinglish-style conversations.

🔎 Semantic Search Demo

Query

"When did everyone finally agree on our vacation?"

ChatMind retrieves:

Priya: Guys Manali fix hai 🏔️

Conversation Context

Ankit   same
Rahul   toh destination final kar dein?
Priya   Guys Manali fix hai 🏔️
Aman    done, tickets dekhte hain
Rohit   finally trip locked 😂

The important point is that the query and retrieved message do not need to share the same wording.

🧪 Decision Threads

The dataset contains three intentionally structured decision conversations.

🏔️ 1. Travel Decision

The group discusses options and ultimately decides on Manali.

💻 2. Project Decision

The group considers multiple project ideas and finally selects a student productivity dashboard.

🌱 3. Presentation Decision

The group discusses the presentation and eventually locks the topic as renewable energy.

These threads are useful for testing multi-message reasoning around decisions, agreements, and confirmations.

📈 Evaluation

ChatMind was evaluated using 40 predefined queries.

32 normal queries

8 hard queries with zero lexical overlap

Current Results

Metric

Score

🥇 Overall Top-1

85.0%

🥈 Normal Top-1

84.4%

🔥 Hard Top-1

87.5%

🎯 Overall Top-5

97.5%

✅ Hard zero-overlap check

PASS

These are the actual results from the project's current evaluation run.

The evaluation compares retrieved messages against the predefined target message IDs.

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

ChatMind/
│
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
│
├── requirements.txt
├── package.json
├── .gitignore
└── README.md

🚀 Run Locally

1. Clone the Repository

git clone https://github.com/rajaji98/ChatMind.git
cd ChatMind

2. Install Node Dependencies

npm install

3. Create a Python Virtual Environment

Windows PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1

4. Install Python Dependencies

pip install -r requirements.txt

5. Start the Server

node .\backend\server.js

Then open:

http://localhost:5000

🔬 Run the Search Engine Directly

You can test the Python search engine without opening the frontend:

python scripts/search_engine.py "What project did the group eventually choose?" --json

📊 Run the Evaluation

Run the full 40-query benchmark:

python scripts/evaluate.py

The script reports retrieval performance for the predefined test set.

💡 Example Queries

Try these in the ChatMind UI:

When did everyone finally agree on our vacation?

What project did the group eventually choose?

What subject was the group's slide deck ultimately secured around?

Which idea survived all the alternatives and became the group's selected build?

Where did the friends eventually settle for their getaway?

🎨 Interface

ChatMind provides a focused dark-themed search experience with:

🌑 Modern dark UI

🔎 Natural-language search

📊 Relevance scoring

👤 Sender and timestamp display

🏷️ Decision / agreement labels

🧵 Thread information

💬 Conversation context

💡 Example query buttons

📱 Responsive layout

🔐 Data & Privacy

The dataset is fully synthetic and was created specifically for evaluating the search system.

It does not represent a real private group conversation.

🧩 Why ChatMind?

Traditional chat search often works best when you already know the exact words used in the original message.

ChatMind targets a harder and more realistic problem:

A user remembers the meaning of a conversation, not the exact sentence.

For example:

User remembers:

"When did everyone finally agree on our vacation?"

Original chat message:

"Guys Manali fix hai 🏔️"

ChatMind bridges that gap with:

Semantic Understanding + Intent-aware Reranking + Conversation Context

🏁 Built For

ITGeeks Vibe Coding Round

Challenge: "Search a Group Chat Properly"

ChatMind was built as a focused semantic retrieval system, rather than a generic chatbot.

🔗 Repository

GitHub: github.com/rajaji98/ChatMind

<div align="center">

🧠 Search the meaning, not just the words.

ChatMind

</div>