from typing import Dict, List

from .metrics import mean_reciprocal_rank, precision_at_k, recall_at_k


def evaluate_rankings(
    predictions: List[str],
    relevant_items: List[str],
    k: int = 5
) -> Dict[str, float]:
    return {
        "precision_at_k": precision_at_k(predictions, relevant_items, k),
        "recall_at_k": recall_at_k(predictions, relevant_items, k),
        "mrr": mean_reciprocal_rank(predictions, relevant_items),
    }
