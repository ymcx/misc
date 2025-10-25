import time
import math


def score(score: int, epoch: float) -> float:
    epoch_current = time.time()
    epoch_diff = epoch_current - epoch

    # Exponential decay
    # Multiplier is 1.0 at 0 hours, 0.5 at ~10 hours
    k = 0.00002
    multiplier = math.exp(-k * epoch_diff)

    return multiplier * score
