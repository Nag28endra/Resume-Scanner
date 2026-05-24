from typing import List


def precision_at_k(predicted: List[str], relevant: List[str], k: int) -> float:
    if k <= 0:
        return 0.0

    top_k = predicted[:k]
    if not top_k:
        return 0.0

    hits = sum(1 for item in top_k if item in relevant)
    return hits / len(top_k)


def recall_at_k(predicted: List[str], relevant: List[str], k: int) -> float:
    if not relevant:
        return 0.0

    top_k = predicted[:k]
    hits = sum(1 for item in top_k if item in relevant)
    return hits / len(relevant)


def mean_reciprocal_rank(predicted: List[str], relevant: List[str]) -> float:
    for index, item in enumerate(predicted, start=1):
        if item in relevant:
            return 1.0 / index
    return 0.0
