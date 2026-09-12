import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))

from search_engine import search, messages

EVALUATION_FILE = ROOT / "backend" / "data" / "evaluations.json"

def normalize(text):
    """Normalize text for lexical-overlap checking."""
    return set(
        re.findall(
            r"[a-z0-9]+",
            text.lower()
        )
    )


def get_message_by_id(message_id):
    for message in messages:
        if message["id"] == message_id:
            return message
    return None


def main():
    print("=" * 50)
    print("CHATMIND EVALUATION")
    print("=" * 50)

    # Load evaluation queries
    if not EVALUATION_FILE.exists():
        print(f"ERROR: Evaluation file not found:")
        print(EVALUATION_FILE)
        return

    with open(EVALUATION_FILE, "r", encoding="utf-8") as f:
        evaluations = json.load(f)

    print(f"\nQueries found: {len(evaluations)}")

    # Validate query count
    normal_queries = [
        q for q in evaluations
        if q["type"] == "normal"
    ]

    hard_queries = [
        q for q in evaluations
        if q["type"] == "hard"
    ]

    print(f"Normal queries: {len(normal_queries)}")
    print(f"Hard queries  : {len(hard_queries)}")

    if len(evaluations) != 40:
        print("\nWARNING: Expected exactly 40 queries.")

    if len(normal_queries) != 32:
        print("WARNING: Expected 32 normal queries.")

    if len(hard_queries) != 8:
        print("WARNING: Expected 8 hard queries.")

    # --------------------------------------------------
    # Check hard-query lexical overlap
    # --------------------------------------------------

    print("\n" + "-" * 50)
    print("HARD QUERY OVERLAP CHECK")
    print("-" * 50)

    overlap_problems = 0

    for q in hard_queries:
        target = get_message_by_id(q["expected_id"])

        if target is None:
            print(f"{q['id']}: TARGET NOT FOUND")
            overlap_problems += 1
            continue

        query_words = normalize(q["query"])
        target_words = normalize(target["text"])

        overlap = query_words & target_words

        if overlap:
            print(
                f"{q['id']}: OVERLAP -> "
                f"{', '.join(sorted(overlap))}"
            )
            overlap_problems += 1
        else:
            print(f"{q['id']}: PASS")

    if overlap_problems == 0:
        print("\nAll 8 hard queries have zero word overlap.")
    else:
        print(
            f"\nWARNING: {overlap_problems} hard queries "
            f"have lexical overlap."
        )

    # --------------------------------------------------
    # Run retrieval evaluation
    # --------------------------------------------------

    print("\n" + "-" * 50)
    print("RUNNING RETRIEVAL TEST")
    print("-" * 50)

    results = []

    for index, q in enumerate(evaluations, start=1):

        retrieved = search(q["query"], top_k=5)

        retrieved_ids = [
            result["id"]
            for result in retrieved
        ]

        expected = q["expected_id"]

        top1_correct = (
            len(retrieved_ids) > 0
            and retrieved_ids[0] == expected
        )

        top5_correct = expected in retrieved_ids

        results.append({
            "id": q["id"],
            "type": q["type"],
            "query": q["query"],
            "expected": expected,
            "top1": top1_correct,
            "top5": top5_correct,
            "returned": retrieved_ids
        })

        status = "✓" if top1_correct else "✗"

        print(
            f"[{index:02d}/40] "
            f"{status} "
            f"{q['id']} - "
            f"{q['query']}"
        )

        if not top1_correct:
            print(
                f"       Expected: {expected}"
            )
            print(
                f"       Got     : "
                f"{retrieved_ids[:3]}"
            )

    # --------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------

    total = len(results)

    normal_results = [
        r for r in results
        if r["type"] == "normal"
    ]

    hard_results = [
        r for r in results
        if r["type"] == "hard"
    ]

    overall_top1 = sum(
        r["top1"] for r in results
    )

    normal_top1 = sum(
        r["top1"] for r in normal_results
    )

    hard_top1 = sum(
        r["top1"] for r in hard_results
    )

    overall_top5 = sum(
        r["top5"] for r in results
    )

    # --------------------------------------------------
    # Final report
    # --------------------------------------------------

    print("\n")
    print("=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)

    if total:
        print(
            f"\nOverall Top-1 Accuracy : "
            f"{overall_top1}/{total} "
            f"({overall_top1 / total * 100:.1f}%)"
        )

    if normal_results:
        print(
            f"Normal Top-1 Accuracy  : "
            f"{normal_top1}/{len(normal_results)} "
            f"({normal_top1 / len(normal_results) * 100:.1f}%)"
        )

    if hard_results:
        print(
            f"Hard Top-1 Accuracy    : "
            f"{hard_top1}/{len(hard_results)} "
            f"({hard_top1 / len(hard_results) * 100:.1f}%)"
        )

    if total:
        print(
            f"Overall Top-5 Accuracy : "
            f"{overall_top5}/{total} "
            f"({overall_top5 / total * 100:.1f}%)"
        )

    print("\n" + "=" * 50)

    # --------------------------------------------------
    # Hard query details
    # --------------------------------------------------

    print("\nHARD QUERY RESULTS")
    print("-" * 50)

    for r in hard_results:
        status = "PASS" if r["top1"] else "FAIL"

        print(
            f"{r['id']} : {status}"
        )

        if not r["top1"]:
            print(
                f"  Expected: {r['expected']}"
            )
            print(
                f"  Returned: {r['returned'][:3]}"
            )

    print("\nEvaluation complete.")


if __name__ == "__main__":
    main()