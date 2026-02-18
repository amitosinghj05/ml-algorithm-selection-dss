from dss.cli_utils import ask_choice, ask_yes_no
from dss.schemas import UserNeeds
from dss.knowledge_base import load_algorithms
from dss.engine import rank_algorithms

def collect_user_needs() -> UserNeeds:
    print("\n=== ML DSS Agent (CLI) ===\n")

    task = ask_choice(
        "What is your problem type?",
        ["classification", "regression", "clustering", "anomaly_detection"]
    )

    data_size = ask_choice(
        "Approximate dataset size?",
        ["small", "medium", "large"]
    )

    interpretability = ask_yes_no("Do you need high interpretability (easy to explain)?")
    accuracy = ask_yes_no("Is maximum accuracy the top priority?")
    fast_training = ask_yes_no("Is fast training important (limited compute / quick iteration)?")

    # adaptive follow-up questions (agent-like)
    text_data = False
    imbalanced = False
    unknown_k = False

    if task == "classification":
        text_data = ask_yes_no("Is your data mainly text (reviews, tickets, emails)?")
        imbalanced = ask_yes_no("Is your dataset imbalanced (one class is rare)?")

    if task == "clustering":
        unknown_k = ask_yes_no("Do you NOT know the number of clusters (k) ahead of time?")

    return UserNeeds(
        task=task,
        data_size=data_size,
        interpretability=interpretability,
        accuracy=accuracy,
        fast_training=fast_training,
        text_data=text_data,
        imbalanced=imbalanced,
        unknown_k=unknown_k
    )

def main():
    needs = collect_user_needs()

    algorithms = load_algorithms("data/knowledge_base.yaml")
    ranked = rank_algorithms(needs, algorithms)

    print("\n--- Top Recommendations ---")
    for i, (algo, score, reasons) in enumerate(ranked[:3], start=1):
        print(f"\n{i}) {algo} (score: {score})")
        for r in reasons[:4]:
            print(f"   - {r}")

    print("\n--- Notes ---")
    print("Ranking is rule-based for consistency and explainability.")
    print("Next step: add more criteria + more algorithms in knowledge_base.yaml.\n")

if __name__ == "__main__":
    main()

