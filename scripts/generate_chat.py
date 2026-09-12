
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

# ============================================================
# CONFIG
# ============================================================

NUM_MESSAGES = 4500

START_DATE = datetime(2026, 3, 1, 9, 0, 0)
END_DATE = datetime(2026, 8, 31, 23, 59, 0)

PARTICIPANTS = [
    "Aman",
    "Priya",
    "Rahul",
    "Neha",
    "Rohit",
    "Sneha",
    "Karan",
    "Ankit",
]

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "backend"
    / "data"
    / "messages.json"
)


# ============================================================
# GENERAL CHAT
# ============================================================

NORMAL_MESSAGES = [
    "bhai kya scene hai?",
    "kal class hai kya?",
    "aaj ka lecture samajh aaya kya?",
    "notes bhej dena please",
    "kisi ke paas assignment hai?",
    "deadline kab hai?",
    "bhai ye question dekh",
    "iska answer kya hai?",
    "I think ye wala approach better hai",
    "kal milte hain",
    "morning everyone",
    "kya kar rahe ho?",
    "lunch ho gaya?",
    "aaj bahut thak gaya yaar",
    "attendance ka kya scene hai?",
    "professor ne kya bola?",
    "presentation ready hai?",
    "slides complete kar di?",
    "file upload kar dena",
    "check kar raha hu",
    "haan bhai bhej",
    "kal discuss karte hain",
    "abhi busy hu",
    "later bro",
    "library mein kaafi rush hai",
    "aaj assignment submit karna hai",
    "kal practical hai",
    "kisi ne lab record complete kiya?",
    "ye concept samajhne mein time lag raha hai",
    "aaj group study karte hain",
    "kaun campus mein hai?",
    "meeting kab rakhni hai?",
    "link bhej do",
    "main check karta hu",
    "thoda wait karo",
    "abhi kaam kar raha hu",
    "raat ko free rahunga",
    "aaj jaldi sona hai",
    "kal morning mein karunga",
]

HINGLISH_MESSAGES = [
    "bhai aaj padhne ka bilkul mood nahi hai",
    "yaar ye topic sar ke upar se ja raha hai",
    "kal se pakka serious study",
    "bhai attendance bach jayegi kya?",
    "sir ne fir se assignment de diya 😭",
    "aaj library chalte hain kya?",
    "chai peene chale?",
    "canteen mein mil?",
    "bhai thoda wait karna",
    "main raste mein hu",
    "traffic bahut hai yaar",
    "ye banda pura confuse kar raha hai",
    "haan samajh gaya ab",
    "mujhe bhi same laga",
    "iska jugaad karna padega",
    "tension mat le ho jayega",
    "kal tak kar denge",
    "bhai deadline close hai",
    "ab toh grind karna padega",
    "aaj raat late tak jagna padega",
    "weekend pe kar lenge",
    "abhi mood nahi hai bro",
    "ye toh mast idea hai",
    "haan ye fix karte hain",
    "kya bolta hai group?",
    "sab agree hain?",
    "mere liye bhi chalega",
    "main confirm karta hu",
    "pehle options compare karte hain",
    "budget dekhna padega",
    "kal final kar denge",
    "ye plan workable hai",
    "mujhe bhi theek lag raha hai",
    "haan isme problem nahi hai",
]

TYPO_MESSAGES = [
    "kal clas hai kya?",
    "bhai send kr dena",
    "mai abhi lib me hu",
    "kya sceene hai?",
    "ha bhai",
    "done broo",
    "ruk 5 min",
    "mai aa rha",
    "ye ques dekh",
    "samjha kya?",
    "mujhe nhi pta",
    "kal pakka",
    "thoda late hoga",
    "bhai plz bhej",
    "ye wala sahi lg rha",
    "kab milna h?",
    "main confirm krta hu",
    "sab ready h?",
]

SHORT_REPLIES = [
    "haan",
    "nah",
    "yep",
    "nope",
    "done",
    "okay",
    "sure",
    "same",
    "+1",
    "lol",
    "nice",
    "cool",
    "perfect",
    "agreed",
    "true",
    "maybe",
    "wait",
]

FORWARDED_MESSAGES = [
    "Forwarded: College notice — registration closes Friday.",
    "Forwarded: Important update regarding tomorrow's lecture.",
    "Forwarded: Scholarship application deadline extended.",
    "Forwarded: Placement cell announcement.",
    "Forwarded: Workshop registration link.",
    "Forwarded: Exam timetable has been updated.",
    "Forwarded: Internship applications open this week.",
    "Forwarded: Department meeting scheduled for Monday.",
]

MEDIA_MESSAGES = [
    "📷 <Media omitted>",
    "🎥 <Video omitted>",
    "📎 <Document omitted>",
    "🎤 <Voice message omitted>",
    "📸 <Image omitted>",
]


# ============================================================
# HELPERS
# ============================================================

def choose_general_message():
    roll = random.random()

    if roll < 0.38:
        return random.choice(NORMAL_MESSAGES)

    if roll < 0.66:
        return random.choice(HINGLISH_MESSAGES)

    if roll < 0.78:
        return random.choice(TYPO_MESSAGES)

    if roll < 0.87:
        return random.choice(SHORT_REPLIES)

    if roll < 0.93:
        return random.choice(FORWARDED_MESSAGES)

    return random.choice(MEDIA_MESSAGES)


def add_message(
    messages,
    sender,
    text,
    timestamp,
    thread_id=None,
    topic="casual",
    message_type="normal",
):
    messages.append({
        "id": "",
        "sender": sender,
        "timestamp": timestamp.isoformat(),
        "text": text,
        "thread_id": thread_id,
        "topic": topic,
        "message_type": message_type,
    })


# ============================================================
# TRAVEL / MANALI THREAD
# ============================================================

def add_manali_thread(messages):

    base = datetime(2026, 5, 14, 18, 10)

    thread_id = "trip_manali"

    thread = [
        ("Rahul", "Guys summer mein kahi trip ka plan banate hain", "discussion"),
        ("Aman", "haan bhai, thoda break milna chahiye", "agreement"),
        ("Neha", "mountains side jaana mujhe better lag raha hai", "proposal"),
        ("Rohit", "Shimla ya Manali dono options hain", "proposal"),
        ("Priya", "Manali better rahega kya?", "question"),
        ("Sneha", "Manali mein June mein weather acha hota hai", "information"),
        ("Karan", "mere exams 17 ko khatam ho rahe hain", "constraint"),
        ("Ankit", "18 ke baad main free hu", "constraint"),
        ("Rahul", "18 se 22 chalega kya sabke liye?", "question"),
        ("Priya", "mere liye dates okay hain", "agreement"),
        ("Aman", "mere liye bhi", "agreement"),
        ("Neha", "haan main bhi free hu", "agreement"),
        ("Rohit", "same here", "agreement"),
        ("Sneha", "18-22 works", "agreement"),
        ("Karan", "haan mere liye bhi chalega", "agreement"),
        ("Ankit", "works for me", "agreement"),
        ("Rahul", "budget around 8-10k rakhte hain", "constraint"),
        ("Priya", "train se jayenge toh cost manageable rahegi", "discussion"),
        ("Aman", "hotel ya hostel pehle check karna padega", "discussion"),
        ("Neha", "maine Mall Road ke paas ek hostel dekha hai", "proposal"),
        ("Rohit", "reviews kaise hain?", "question"),
        ("Neha", "4.4 rating hai aur rooms bhi decent hain", "information"),
        ("Sneha", "location bhi convenient lag rahi hai", "agreement"),
        ("Karan", "mujhe chalega", "agreement"),
        ("Ankit", "same", "agreement"),
        ("Rahul", "toh destination final kar dein?", "decision_question"),
        ("Priya", "Guys Manali fix hai 🏔️", "decision"),
        ("Aman", "done, tickets dekhte hain", "decision_confirmation"),
        ("Rohit", "finally trip locked 😂", "decision_confirmation"),
        ("Sneha", "Manali it is", "decision_confirmation"),
    ]

    for i, (sender, text, msg_type) in enumerate(thread):

        add_message(
            messages,
            sender,
            text,
            base + timedelta(minutes=i * 3),
            thread_id,
            "travel",
            msg_type,
        )


# ============================================================
# PROJECT THREAD
# ============================================================

def add_project_thread(messages):

    base = datetime(2026, 4, 9, 19, 20)

    thread_id = "project_productivity"

    thread = [
        ("Aman", "project ke liye topic decide karna hai", "decision_question"),
        ("Priya", "attendance tracker bana sakte hain", "proposal"),
        ("Rahul", "thoda common nahi ho jayega?", "concern"),
        ("Neha", "expense tracker bhi option hai", "proposal"),
        ("Rohit", "AI based kuch interesting rahega", "proposal"),
        ("Sneha", "recommendation system kaisa hai?", "proposal"),
        ("Karan", "scope bahut bada ho jayega", "concern"),
        ("Ankit", "simple rakho warna deadline mein fasenge", "constraint"),
        ("Priya", "student productivity dashboard bana lete hain", "proposal"),
        ("Aman", "isme study hours aur task tracking add kar sakte hain", "discussion"),
        ("Rahul", "charts bhi useful rahenge", "agreement"),
        ("Neha", "database simple tables se manage ho jayega", "agreement"),
        ("Rohit", "frontend bhi acha ban jayega", "agreement"),
        ("Sneha", "everyone okay with productivity dashboard?", "decision_question"),
        ("Karan", "haan", "agreement"),
        ("Ankit", "works", "agreement"),
        ("Rahul", "mujhe bhi ye option practical lag raha hai", "agreement"),
        ("Priya", "then student productivity dashboard final", "decision"),
        ("Aman", "locked 🔒", "decision_confirmation"),
        ("Neha", "okay dashboard hi banate hain", "decision_confirmation"),
    ]

    for i, (sender, text, msg_type) in enumerate(thread):

        add_message(
            messages,
            sender,
            text,
            base + timedelta(minutes=i * 4),
            thread_id,
            "project",
            msg_type,
        )


# ============================================================
# RENEWABLE ENERGY THREAD
# ============================================================

def add_presentation_thread(messages):

    base = datetime(2026, 6, 3, 20, 5)

    thread_id = "presentation_renewable"

    thread = [
        ("Rahul", "presentation Friday ko hai", "information"),
        ("Neha", "topic renewable energy hai na?", "question"),
        ("Priya", "haan renewable energy hi hai", "agreement"),
        ("Aman", "slides kitni banani hain?", "question"),
        ("Sneha", "sir ne bola maximum 12", "constraint"),
        ("Rohit", "introduction main kar lunga", "assignment"),
        ("Karan", "solar wala section mujhe de do", "assignment"),
        ("Ankit", "wind energy main handle karunga", "assignment"),
        ("Priya", "data aur conclusion main karungi", "assignment"),
        ("Rahul", "graphs kaun banayega?", "question"),
        ("Aman", "graphs main bana dunga", "assignment"),
        ("Neha", "good", "agreement"),
        ("Sneha", "Wednesday night tak complete karna", "deadline"),
        ("Rohit", "okay", "agreement"),
        ("Karan", "done", "agreement"),
        ("Ankit", "works for me", "agreement"),
        ("Priya", "Wednesday ko final presentation lock kar dete hain", "decision"),
        ("Rahul", "haan final kar do", "agreement"),
        ("Aman", "renewable energy presentation locked", "decision_confirmation"),
    ]

    for i, (sender, text, msg_type) in enumerate(thread):

        add_message(
            messages,
            sender,
            text,
            base + timedelta(minutes=i * 3),
            thread_id,
            "renewable_energy",
            msg_type,
        )


# ============================================================
# GENERATE
# ============================================================

def generate():

    messages = []

    current_time = START_DATE

    # --------------------------------------------------------
    # GENERAL CHAT
    # --------------------------------------------------------

    while len(messages) < NUM_MESSAGES:

        sender = random.choice(PARTICIPANTS)

        current_time += timedelta(
            minutes=random.randint(2, 180)
        )

        if current_time > END_DATE:

            current_time = (
                START_DATE
                + timedelta(
                    minutes=random.randint(0, 260000)
                )
            )

        add_message(
            messages,
            sender,
            choose_general_message(),
            current_time,
            None,
            "casual",
            "normal",
        )

    # --------------------------------------------------------
    # ADD IMPORTANT THREADS
    # --------------------------------------------------------

    add_manali_thread(messages)

    add_project_thread(messages)

    add_presentation_thread(messages)

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    messages.sort(
        key=lambda x: x["timestamp"]
    )

    # --------------------------------------------------------
    # REASSIGN IDS
    # --------------------------------------------------------

    for index, message in enumerate(
        messages,
        start=1
    ):
        message["id"] = f"msg_{index:04d}"

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            messages,
            f,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    decision_count = sum(
        1
        for message in messages
        if message["message_type"]
        in {
            "decision",
            "decision_confirmation",
        }
    )

    thread_count = sum(
        1
        for message in messages
        if message["thread_id"] is not None
    )

    print("=" * 55)
    print("CHATMIND DATASET GENERATED")
    print("=" * 55)
    print(f"Messages          : {len(messages)}")
    print(f"People            : {len(PARTICIPANTS)}")
    print(f"Thread messages   : {thread_count}")
    print(f"Decision messages : {decision_count}")
    print(f"Output            : {OUTPUT}")
    print("=" * 55)


if __name__ == "__main__":
    generate()
