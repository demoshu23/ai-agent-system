from typing import List, Dict
import httpx


async def evaluate_runs(runs: List[Dict]) -> Dict:
    # placeholder – plug in Ragas / DeepEval later
    scores = []
    for r in runs:
        # naive: length of result as proxy for completeness
        result = r.get("result", "") or ""
        scores.append(len(result))

    avg = sum(scores) / max(len(scores), 1)
    return {"avg_length_score": avg, "runs": len(runs)}
