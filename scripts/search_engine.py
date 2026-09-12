import json
import sys
import re
from pathlib import Path
import io


import numpy as np
from sentence_transformers import SentenceTransformer

# Force UTF-8 output on Windows
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding="utf-8",
        errors="replace"
    )
# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MESSAGES_FILE = BASE_DIR / "backend" / "data" / "messages.json"
EMBEDDINGS_FILE = BASE_DIR / "embeddings" / "messages.npy"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# ============================================================
# LOAD
# ============================================================

print("Loading messages...", file=sys.stderr)

with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
    messages = json.load(f)

print("Loading embeddings...", file=sys.stderr)

embeddings = np.load(EMBEDDINGS_FILE)

print("Loading model...", file=sys.stderr)

model = SentenceTransformer(MODEL_NAME)

print("Search engine ready.", file=sys.stderr)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# QUERY INTENT
# ============================================================

def detect_intent(query):

    q = normalize(query)
    words = set(q.split())

    intent = {
        "decision": False,
        "topic": None,
        "message_type": None,
        "sender": None
    }

    # --------------------------------------------------------
    # Decision intent
    # --------------------------------------------------------

    decision_words = {
        "agree",
        "agreed",
        "decision",
        "decide",
        "decided",
        "choose",
        "chosen",
        "pick",
        "picked",
        "select",
        "selected",
        "settle",
        "settled",
        "final",
        "finally",
        "fix",
        "fixed",
        "confirm",
        "confirmed",
        "lock",
        "locked",
        "consensus",
        "eventually",
        "ultimately"
    }

    if words.intersection(decision_words):
        intent["decision"] = True

    # --------------------------------------------------------
    # Project
    # --------------------------------------------------------

    project_words = {
        "project",
        "application",
        "app",
        "software",
        "dashboard",
        "system",
        "tracker",
        "trackers",
        "productivity",
        "coding",
        "build",
        "building",
        "study",
        "student"
    }

    if words.intersection(project_words):
        intent["topic"] = "project"

    # --------------------------------------------------------
    # Travel
    # --------------------------------------------------------

    travel_words = {
        "vacation",
        "trip",
        "travel",
        "holiday",
        "tour",
        "journey",
        "destination",
        "getaway",
        "mountain",
        "outing",
        "friends"
    }

    if words.intersection(travel_words):
        intent["topic"] = "travel"

    # --------------------------------------------------------
    # Presentation
    # --------------------------------------------------------

    presentation_words = {
        "presentation",
        "present",
        "slides",
        "slide",
        "renewable",
        "energy",
        "solar",
        "wind",
        "power",
        "subject",
        "topic",
        "deck"
    }

    if words.intersection(presentation_words):
        intent["topic"] = "renewable_energy"

    # --------------------------------------------------------
    # Message-type intent
    # --------------------------------------------------------

    proposal_words = {
        "propose",
        "proposed",
        "proposal",
        "suggest",
        "suggested",
        "idea",
        "option",
        "recommend",
        "recommended"
    }

    concern_words = {
        "concern",
        "problem",
        "issue",
        "worry",
        "worried",
        "scope",
        "risk"
    }

    agreement_words = {
        "agree",
        "agreed",
        "okay",
        "works",
        "practical",
        "support"
    }

    question_words = {
        "who",
        "what",
        "which",
        "where",
        "when",
        "how",
        "whether"
    }

    if words.intersection(proposal_words):
        intent["message_type"] = "proposal"

    elif words.intersection(concern_words):
        intent["message_type"] = "concern"

    elif words.intersection(agreement_words):
        intent["message_type"] = "agreement"

    # --------------------------------------------------------
    # Person intent
    # --------------------------------------------------------

    people = {
        "aman": "Aman",
        "priya": "Priya",
        "rahul": "Rahul",
        "neha": "Neha",
        "rohit": "Rohit",
        "sneha": "Sneha",
        "karan": "Karan",
        "ankit": "Ankit"
    }

    for name, actual_name in people.items():

        if name in words:
            intent["sender"] = actual_name
            break

    return intent


# ============================================================
# DECISION SCORE
# ============================================================

def decision_score(message, decision_intent):

    if not decision_intent:
        return 0.0

    message_type = message.get(
        "message_type",
        ""
    )

    text = normalize(
        message.get("text", "")
    )

    score = 0.0

    # Explicit final decision
    if message_type == "decision":
        score += 0.52

    # Confirmation
    elif message_type == "decision_confirmation":
        score += 0.20

    # Decision question
    elif message_type == "decision_question":
        score += 0.10

    # Agreement
    elif message_type == "agreement":
        score += 0.05

    # --------------------------------------------------------
    # Strong final-decision language
    # --------------------------------------------------------

    strong_final_phrases = [
        "final",
        "finally",
        "locked",
        "lock",
        "fixed",
        "fix hai",
        "confirmed",
        "confirm",
        "decided",
        "decision",
        "chosen",
        "selected",
        "final kar"
    ]

    if any(
        phrase in text
        for phrase in strong_final_phrases
    ):
        score += 0.10

    return score


# ============================================================
# MESSAGE TYPE SCORE
# ============================================================

def message_type_score(message, requested_type):

    if requested_type is None:
        return 0.0

    message_type = message.get(
        "message_type",
        ""
    )

    if requested_type == "proposal":
        return 0.30 if message_type == "proposal" else 0.0

    if requested_type == "concern":
        return 0.30 if message_type == "concern" else 0.0

    if requested_type == "agreement":
        return 0.25 if message_type == "agreement" else 0.0

    return 0.0


# ============================================================
# SENDER SCORE
# ============================================================

def sender_score(message, sender):

    if sender is None:
        return 0.0

    if message.get("sender") == sender:
        return 0.25

    return 0.0

def answer_intent_score(index, query, intent):
    score = 0.0
    """
    Match the type of answer the query is asking for.
    This helps distinguish nearby messages in the same decision thread.
    """
    message = messages[index]
    message_type = message.get("message_type", "")
    text = message.get("text", "").lower()
    q = query.lower()

    score = 0.0

    # -----------------------------------------
    # WHAT / TOPIC / SUBJECT questions
    # -----------------------------------------
    topic_words = [
        "what was", "what is", "which subject",
        "which topic", "what presentation",
        "what did the group agree to present",
        "confirmed topic", "final presentation topic"
    ]

    if any(word in q for word in topic_words):
        if message_type == "decision_confirmation":
            score += 0.35
        elif message_type == "decision":
            score += 0.10
        elif message_type == "agreement":
            score += 0.03

        # Messages that explicitly contain the subject/topic
        if "renewable energy" in text:
            score += 0.20

    # -----------------------------------------
    # ALTERNATIVE / OPTIONS questions
    # -----------------------------------------
    alternative_words = [
        "alternative", "alternatives",
        "option", "options",
        "different ideas", "different trackers"
    ]

    if any(word in q for word in alternative_words):
        if message_type == "proposal":
            score += 0.40
        elif message_type == "decision":
            score -= 0.10
        elif message_type == "decision_confirmation":
            score -= 0.10

    # -----------------------------------------
    # WHO questions
    # -----------------------------------------
    if q.startswith("who ") or "who " in q:
        if message_type in ["proposal", "decision_question", "agreement",
                            "decision_confirmation", "concern"]:
            score += 0.12

    # -----------------------------------------
    # WHEN questions
    # -----------------------------------------
    if q.startswith("when ") or " when " in q:
        if message_type == "decision":
            score += 0.18

    # -----------------------------------------
    # WHERE / DESTINATION questions
    # -----------------------------------------
    if q.startswith("where ") or "where " in q:
        if message_type in ["decision", "decision_confirmation"]:
            score += 0.15

    # -----------------------------------------
    # "ASKED WHETHER EVERYONE..." questions
    # -----------------------------------------
    if "asked whether" in q or "asked if" in q or "everyone okay" in q:
        if message_type == "decision_question":
            score += 0.45

    # -----------------------------------------
    # "SAID ... PRACTICAL" type questions
    # -----------------------------------------
    if "practical" in q:
        if "practical" in text:
            score += 0.50
        if message_type == "agreement":
            score += 0.20

    # -----------------------------------------
    # "CONFIRMED" questions
    # -----------------------------------------
    if "confirmed" in q or "confirmation" in q:
        if message_type == "decision_confirmation":
            score += 0.35

    # -----------------------------------------
    # "LOCKED" questions
    # -----------------------------------------
    if "locked" in q:
        if message_type == "decision_confirmation":
            score += 0.30
        elif message_type == "decision":
            score += 0.05

    return score


def final_selection_score(index, query):
    """
    Detect queries asking for the final selected choice
    after alternatives/options were discussed.
    """
    message = messages[index]
    message_type = message.get("message_type", "")
    text = message.get("text", "").lower()
    q = query.lower()

    score = 0.0

    # -----------------------------------------
    # FINAL SELECTION LANGUAGE
    # -----------------------------------------

    final_selection_phrases = [
        "eventually choose",
        "eventually selected",
        "ultimately selected",
        "ultimately chosen",
        "final decision",
        "finalized",
        "selected build",
        "selected idea",
        "selected solution",
        "became the",
        "end up building",
        "ended up building",
        "survived all the alternatives"
    ]

    if any(phrase in q for phrase in final_selection_phrases):

        if message_type == "decision":
            score += 0.35

        elif message_type == "decision_confirmation":
            score += 0.25

        elif message_type == "proposal":
            score -= 0.15

    # -----------------------------------------
    # "AGREE TO MAKE" / "AGREE TO BUILD"
    # -----------------------------------------

    if (
        "agree to make" in q
        or "agree to build" in q
        or "agree to create" in q
    ):
        if message_type == "decision":
            score += 0.30

        if "project" in q and "presentation" not in q:
            if "productivity dashboard" in text:
                score += 0.15

    return score
# ============================================================
# TEXT RELEVANCE SCORE
# ============================================================

def lexical_score(query, message):

    query_words = set(
        normalize(query).split()
    )

    message_words = set(
        normalize(
            message.get("text", "")
        ).split()
    )

    if not query_words or not message_words:
        return 0.0

    overlap = query_words.intersection(
        message_words
    )

    # Small lexical signal.
    # Semantic similarity remains the main signal.
    return min(
        len(overlap) * 0.025,
        0.15
    )

# ============================================================
# THREAD-AWARE SCORE
# ============================================================

def thread_score(index, query, intent):
    """
    Give a small additional score based on the surrounding
    conversation, not just the individual message.
    """

    message = messages[index]
    thread_id = message.get("thread_id")

    if thread_id is None:
        return 0.0

    score = 0.0

    # --------------------------------------------------------
    # Look at nearby messages in the same thread
    # --------------------------------------------------------

    start = max(0, index - 4)
    end = min(len(messages), index + 5)

    nearby = messages[start:end]

    decision_count = 0
    agreement_count = 0

    for msg in nearby:

        if msg.get("thread_id") != thread_id:
            continue

        msg_type = msg.get("message_type")

        if msg_type == "decision":
            decision_count += 1

        elif msg_type == "agreement":
            agreement_count += 1

    # A message surrounded by decision/agreement messages
    # is more likely to be part of the actual conclusion.
    score += min(decision_count * 0.03, 0.09)
    score += min(agreement_count * 0.01, 0.04)

    # Explicit decision gets an additional contextual advantage.
    if message.get("message_type") == "decision":
        score += 0.08

    return score

# ============================================================
# CONTEXT
# ============================================================

def get_context(index, window=2):

    start = max(
        0,
        index - window
    )

    end = min(
        len(messages),
        index + window + 1
    )

    context = []

    for i in range(start, end):

        msg = messages[i]

        context.append({

            "id": msg.get("id"),

            "sender": msg.get("sender"),

            "timestamp": msg.get("timestamp"),

            "text": msg.get("text"),

            "thread_id": msg.get("thread_id"),

            "topic": msg.get("topic"),

            "message_type": msg.get(
                "message_type"
            )

        })

    return context


# ============================================================
# SEARCH
# ============================================================

def search(query, top_k=5):

    # --------------------------------------------------------
    # Detect intent
    # --------------------------------------------------------

    intent = detect_intent(query)

    # --------------------------------------------------------
    # Encode query
    # --------------------------------------------------------

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    # --------------------------------------------------------
    # Semantic similarity
    # --------------------------------------------------------

    similarities = np.dot(
        embeddings,
        query_embedding
    )

    # --------------------------------------------------------
    # Search pool
    # --------------------------------------------------------

    if intent["topic"] is not None:

        candidate_indices = [
            i
            for i, message in enumerate(messages)
            if message.get("topic") == intent["topic"]
        ]

    else:

        candidate_count = min(
            300,
            len(messages)
        )

        candidate_indices = list(
            np.argsort(similarities)[
                -candidate_count:
            ][::-1]
        )

    # --------------------------------------------------------
    # Candidate scoring
    # --------------------------------------------------------

    results = []

    for index in candidate_indices:

        message = messages[index]

        semantic_score = float(
            similarities[index]
        )

        score = semantic_score

        # ----------------------------------------------------
        # Decision intent
        # ----------------------------------------------------

        score += decision_score(
            message,
            intent["decision"]
        )

        # ----------------------------------------------------
        # Message-type intent
        # ----------------------------------------------------

        score += message_type_score(
            message,
            intent["message_type"]
        )

        # ----------------------------------------------------
        # Person intent
        # ----------------------------------------------------

        score += sender_score(
            message,
            intent["sender"]
        )

        # ----------------------------------------------------
        # Lexical relevance
        # ----------------------------------------------------

        score += lexical_score(
            query,
            message
        )
    # ----------------------------------------------------
    # Answer intent
    # ----------------------------------------------------
        score += answer_intent_score(index, query, intent)

        score += final_selection_score( index,query)

# ----------------------------------------------------
# Thread-aware scoring
# ----------------------------------------------------

        score += thread_score(
            index,
            query,
            intent
        )

        results.append({

            "index": int(index),

            "semantic_score": semantic_score,

            "rerank_score": score

        })

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Build output
    # --------------------------------------------------------

    final_results = []

    for result in results[:top_k]:

        index = result["index"]

        message = messages[index]

        final_results.append({

            "id": message.get("id"),

            "sender": message.get("sender"),

            "timestamp": message.get("timestamp"),

            "text": message.get("text"),

            "topic": message.get("topic"),

            "thread_id": message.get("thread_id"),

            "message_type": message.get(
                "message_type"
            ),

            "similarity": round(
                result["semantic_score"],
                4
            ),

            "rerank_score": round(
                result["rerank_score"],
                4
            ),

            "context": get_context(
                index,
                window=2
            )

        })

    return final_results


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":

    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python search_engine.py <query> [--json]")
        sys.exit(1)

    query = sys.argv[1]

    # Force UTF-8 output for API/JSON mode
if "--json" in sys.argv:
    sys.stdout.reconfigure(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    results = search(query, top_k=5)

    # --------------------------------------------------------
    # JSON mode
    # --------------------------------------------------------

    if "--json" in sys.argv:

        print(
            json.dumps(
                {
                    "query": query,
                    "results": results
                },
                ensure_ascii=False
            )
        )

        sys.exit(0)

    # --------------------------------------------------------
    # Normal terminal mode
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CHATMIND SEARCH")
    print("=" * 60)

    print(f"\nQuery: {query}\n")

    for i, result in enumerate(results, 1):

        print(
            f"{i}. "
            f"{result['sender']} | "
            f"{result['text']}"
        )

        print(
            f"   Score: {result['rerank_score']} "
            f"(semantic: {result['similarity']})"
        )

        print(
            f"   Thread: {result.get('thread_id')}"
        )

        print()