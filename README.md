# 🧠 ChatMind --- Intelligent Group Chat Search

> **Search thousands of group-chat messages by meaning, not just
> keywords.**

ChatMind is a semantic group-chat retrieval system built for the
**ITGeeks Vibe Coding Round** challenge.

Instead of behaving like a chatbot, ChatMind focuses on one practical
problem:

**"I remember we discussed something in the group, but I don't remember
the exact words. Can I find it?"**

ChatMind answers this by combining multilingual sentence embeddings,
semantic similarity, intent-aware reranking, and conversation context.

------------------------------------------------------------------------

## 📌 Overview

Group chats become difficult to search as they grow.

A keyword search can fail when the user remembers the **meaning** of a
conversation but not the exact wording.

For example:

> **Query:** "What project did the group eventually choose?"

The actual message may say:

> "then student productivity dashboard final"

There is no exact keyword match for the entire question, but the
semantic meaning is strongly related.

ChatMind is designed to retrieve that message and show the surrounding
conversation so the user can understand **why and how the decision was
made**.

------------------------------------------------------------------------

## ✨ Features

### 🔎 Semantic Search

Searches messages based on meaning using sentence embeddings rather than
relying only on exact keywords.

### 🧠 Intent-Aware Retrieval

The search engine detects useful signals such as:

-   Decision-related queries
-   Message type
-   Sender references
-   Lexical similarity
-   Answer intent
-   Thread relevance

These signals are combined with embedding similarity to improve ranking.

### 🧵 Conversation Context

Results include surrounding messages from the same conversation thread,
making it easier to understand the complete discussion.

### 📊 Relevance Scores

Each result displays a relevance/reranking score so users can see how
strongly the system matched the query.

### 🌐 Multilingual / Hinglish-Friendly

The dataset contains realistic informal group-chat language, including
Hinglish, typos, short messages, and casual expressions.

### ⚡ Simple Web Interface

A clean browser interface allows users to enter natural-language
questions and inspect retrieved messages.

------------------------------------------------------------------------

## 🎯 Challenge Requirements

ChatMind was designed around the following retrieval challenge:

-   Search a large group chat
-   Support natural-language queries
-   Handle semantic/paraphrased questions
-   Retrieve important decisions from conversations
-   Show useful surrounding context
-   Demonstrate evaluation on normal and difficult queries
-   Avoid relying only on keyword overlap

------------------------------------------------------------------------

## 📊 Dataset

The generated dataset contains:

  Property                                   Value
  --------------------- --------------------------
  Total messages                         **4,569**
  Participants                               **8**
  Decision threads                           **3**
  Thread messages                           **69**
  Embedding dimension                      **384**
  Date range              **March -- August 2026**

### Participants

-   Aman
-   Priya
-   Rahul
-   Neha
-   Rohit
-   Sneha
-   Karan
-   Ankit

### Main Decision Threads

1.  🏔️ **Manali Trip**
2.  💻 **Student Productivity Dashboard**
3.  🌱 **Renewable Energy Presentation**

The remaining messages simulate normal group-chat activity so that the
search engine has to find relevant messages inside a larger noisy
dataset.

------------------------------------------------------------------------

## 🧠 How ChatMind Works

The complete retrieval pipeline is:

``` text
User Query
    ↓
Node.js / Express API
    ↓
Python Search Engine
    ↓
SentenceTransformer Embedding
    ↓
Semantic Similarity Search
    ↓
Intent + Metadata Reranking
    ↓
Top Relevant Messages
    ↓
Conversation Context
    ↓
Frontend Result Cards
```

### 🔄 Search Pipeline

#### Step 1 --- User Query

The user enters a natural-language question such as:

> "What project did the group eventually choose?"

#### Step 2 --- API Request

The browser sends the query to the Node.js/Express backend.

``` text
POST /api/search
```

#### Step 3 --- Query Embedding

The Python search engine converts the query into a vector using:

``` text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

#### Step 4 --- Semantic Retrieval

The query vector is compared against the precomputed message embeddings
using vector similarity.

This allows paraphrases to match even when they do not share the same
words.

#### Step 5 --- Reranking

Retrieved messages are reranked using multiple signals:

``` text
Semantic Similarity
        +
Decision Score
        +
Message Type
        +
Sender Match
        +
Lexical Similarity
        +
Answer Intent
        +
Final Selection Score
        +
Thread Relevance
```

#### Step 6 --- Context Retrieval

Once a relevant message is selected, nearby messages from the same
conversation thread are returned as context.

#### Step 7 --- Frontend Display

The browser displays:

-   Sender
-   Timestamp
-   Message
-   Topic
-   Thread
-   Relevance score
-   Conversation context

------------------------------------------------------------------------

## 🤖 Embedding Model

ChatMind uses:

**`paraphrase-multilingual-MiniLM-L12-v2`**

The model produces **384-dimensional sentence embeddings**.

This is particularly useful for the dataset because the chat contains
informal English, Hinglish, and paraphrased expressions.

------------------------------------------------------------------------

## 🔎 Semantic Search Example

### Query

> "What did the group decide to build?"

### Retrieved Message

> **Priya:** "then student productivity dashboard final"

### Context

The surrounding discussion includes proposals such as:

-   Attendance tracker
-   Expense tracker
-   Recommendation system
-   Student productivity dashboard

The conversation eventually reaches:

> "everyone okay with productivity dashboard?"

followed by agreement and the final decision.

This demonstrates why context is important: the system is not simply
finding a keyword --- it is retrieving the message that represents the
final decision.

------------------------------------------------------------------------

## 🧪 Decision Threads

### 💻 Project Decision

The group considered several project ideas:

-   Attendance tracker
-   Expense tracker
-   AI-based ideas
-   Recommendation system
-   Student productivity dashboard

The group eventually selected:

**Student Productivity Dashboard**

The decision was confirmed in the conversation.

------------------------------------------------------------------------

### 🏔️ Travel Decision

The dataset contains a vacation discussion where the group eventually
settles on:

**Manali**

This thread is useful for testing semantic queries such as:

> "Where did the friends eventually settle for their getaway?"

------------------------------------------------------------------------

### 🌱 Presentation Decision

The presentation discussion eventually confirms:

**Renewable Energy**

Example query:

> "What subject was the group's slide deck ultimately secured around?"

The search engine is expected to retrieve the final presentation
confirmation and its surrounding context.

------------------------------------------------------------------------

## 📈 Evaluation

ChatMind includes a small evaluation benchmark containing:

-   **32 normal queries**
-   **8 hard queries**
-   **40 total queries**

The hard queries intentionally use different wording and are designed to
test semantic understanding rather than simple keyword matching.

### Current Results

  Metric                                              Result
  ---------------------------------- -----------------------
  Overall Top-1                        **34 / 40 --- 85.0%**
  Normal Top-1                         **27 / 32 --- 84.4%**
  Hard Top-1                             **7 / 8 --- 87.5%**
  Overall Top-5                        **39 / 40 --- 97.5%**
  Hard-query lexical-overlap check                  **PASS**

The results demonstrate that the retrieval pipeline can identify
relevant messages even when the query wording differs substantially from
the original chat message.

------------------------------------------------------------------------

## 🛠️ Tech Stack

### Frontend

-   HTML5
-   CSS3
-   JavaScript

### Backend

-   Node.js
-   Express.js
-   CORS

### Search / AI

-   Python
-   NumPy
-   Sentence Transformers
-   `paraphrase-multilingual-MiniLM-L12-v2`

### Data

-   JSON
-   NumPy `.npy` embeddings

### Development

-   Git
-   GitHub
-   VS Code

------------------------------------------------------------------------

## 📁 Project Structure

``` text
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
│   └── messages.npy
│
├── requirements.txt
├── package.json
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

## 🚀 Run Locally

### 1. Clone the repository

``` bash
git clone https://github.com/rajaji98/ChatMind.git
cd ChatMind
```

### 2. Install Node.js dependencies

``` bash
npm install
```

### 3. Create and activate Python environment

Windows:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

``` bash
pip install -r requirements.txt
```

### 5. Start the backend

``` bash
node backend/server.js
```

The application will be available at:

``` text
http://localhost:5000
```

------------------------------------------------------------------------

## 🔬 Run the Search Engine Directly

You can test the Python search engine without the web interface:

``` bash
python scripts/search_engine.py "What project did the group eventually choose?"
```

For JSON output:

``` bash
python scripts/search_engine.py "What project did the group eventually choose?" --json
```

------------------------------------------------------------------------

## 📊 Run the Evaluation

Run the benchmark with:

``` bash
python scripts/evaluate.py
```

The evaluation compares the retrieved results against the expected
target messages and reports Top-1 and Top-5 retrieval performance.

------------------------------------------------------------------------

## 💡 Example Queries

Try questions like:

``` text
What project did the group eventually choose?
```

``` text
Which destination did the group settle on?
```

``` text
What presentation was locked?
```

``` text
Who proposed the productivity dashboard?
```

``` text
What alternatives were discussed for the project?
```

``` text
Who raised a concern about the project scope?
```

``` text
What did Ankit say about keeping the project simple?
```

``` text
Where did the friends eventually settle for their getaway?
```

------------------------------------------------------------------------

## 🎨 Interface

ChatMind provides a dark, modern search interface designed around the
core retrieval workflow.

The interface includes:

-   🔍 Natural-language search
-   📊 Dataset message count
-   🏷️ Topic and message-type tags
-   ⭐ Relevance scores
-   🧵 Conversation context
-   📱 Responsive layout
-   💬 Example queries

------------------------------------------------------------------------

## 🔐 Data & Privacy

ChatMind uses a generated synthetic group-chat dataset for demonstration
and evaluation.

No private real-world conversations are required to run the project.

------------------------------------------------------------------------

## 🧩 Why ChatMind?

Traditional chat search often expects users to remember the exact words
that appeared in a message.

Real conversations do not work that way.

You may remember:

> "We talked about the project we were going to build..."

while the actual message says:

> "then student productivity dashboard final"

ChatMind bridges this gap through semantic retrieval.

### The key idea

**Search the conversation by what you remember, not just by what was
written.**

------------------------------------------------------------------------

## 🏁 Built For

**ITGeeks --- Vibe Coding Round**

Project challenge:

> **Search a Group Chat Properly**

ChatMind was built as a focused retrieval system rather than a
general-purpose chatbot.

------------------------------------------------------------------------

## 🔗 GitHub Repository

**Repository:**\
https://github.com/rajaji98/ChatMind

------------------------------------------------------------------------

## 👨‍💻 Author

**Arun Singh**

Built with Python, Node.js, JavaScript, and a lot of debugging. 🚀

------------------------------------------------------------------------

⭐ If you find the project interesting, consider giving the repository a
star!
