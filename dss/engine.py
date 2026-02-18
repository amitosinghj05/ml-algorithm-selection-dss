from typing import Dict, List, Tuple
from dss.schemas import UserNeeds
from dss.knowledge_base import Family


def add_score(scores: Dict[str, int], reasons: Dict[str, List[str]], key: str, pts: int, reason: str) -> None:
    scores[key] += pts
    reasons[key].append(reason)


def rank_families(needs: UserNeeds, families: List[Family]) -> List[Tuple[str, int, List[str], List[str]]]:


    scores = {f.name: 0 for f in families}
    reasons = {f.name: [] for f in families}


    W_MODALITY = 8
    W_DOMAIN = 4

    for f in families:

        if needs.modality in f.modalities:
            add_score(scores, reasons, f.name, W_MODALITY, f"Matches data modality: {needs.modality}")
        else:
            add_score(scores, reasons, f.name, -W_MODALITY, f"Does not match modality: {needs.modality}")


        if needs.domain in f.domains:
            add_score(scores, reasons, f.name, W_DOMAIN, f"Commonly used in domain: {needs.domain}")


        if needs.goal == "clustering":
            if "unsupervised" in f.tags:
                add_score(scores, reasons, f.name, 4, "Designed for unsupervised clustering")
        elif needs.goal == "anomaly_detection":
            if "anomaly" in f.tags:
                add_score(scores, reasons, f.name, 4, "Designed for anomaly detection")
        else:

            if "baseline" in f.tags:
                add_score(scores, reasons, f.name, 1, "Useful baseline for supervised learning")
            if "high_accuracy" in f.tags:
                add_score(scores, reasons, f.name, 1, "Often strong performance in supervised settings")


        if needs.interpretability:
            if "interpretable" in f.tags:
                add_score(scores, reasons, f.name, 4, "Supports interpretability requirement")
            else:
                add_score(scores, reasons, f.name, -2, "Less interpretable than simpler models")

        if needs.privacy_sensitive:
            if "privacy_sensitive" in f.tags or "governance" in f.tags:
                add_score(scores, reasons, f.name, 5, "Aligns with privacy / governance constraints")

            if "needs_compute" in f.tags:
                add_score(scores, reasons, f.name, -1, "May require centralized training resources (privacy review needed)")

        if needs.limited_labels:
            if "limited_labels" in f.tags or "transfer_learning" in f.tags or "no_labels" in f.tags:
                add_score(scores, reasons, f.name, 4, "Works well when labeled data is limited")

        if needs.real_time:

            if "fast_infer" in f.tags:
                add_score(scores, reasons, f.name, 3, "Suitable for low-latency / real-time use")
            if "needs_compute" in f.tags:
                add_score(scores, reasons, f.name, -1, "May be heavier for real-time constraints")


        if f.notes:
            reasons[f.name].append(f"Note: {f.notes[0]}")

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for name, score in ranked:
        if score <= 0:
            continue
        family = next(ff for ff in families if ff.name == name)
        results.append((name, score, reasons[name], family.examples))

    return results

