"""Interpretable, corpus-trained event expectancy baseline.

This is *not* IDyOM. It is a small variable-order probabilistic baseline for
testing the scientific utility of entropy and surprisal before choosing a
research-grade expectation implementation. It predicts symbolic event tokens,
not emotions, and must be trained on a corpus disjoint from evaluation works.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Hashable, Iterable, Sequence


Token = Hashable
_UNSEEN = object()


@dataclass(frozen=True)
class Expectation:
    index: int
    event: str
    probability: float
    surprisal_bits: float
    entropy_bits_before: float
    context_length: int

    def to_dict(self) -> dict:
        return asdict(self)


class VariableOrderExpectancy:
    """Hierarchically smoothed n-gram model with explicit information measures.

    Each order's empirical distribution is interpolated with the lower order
    via a Dirichlet-style backoff. `unseen` is an explicit bucket for events
    absent from training. A model is frozen after `fit`; evaluation does not
    change the corpus statistics.
    """

    def __init__(self, max_order: int = 3, smoothing: float = 1.0):
        if max_order < 0 or not isinstance(max_order, int):
            raise ValueError("max_order must be a nonnegative integer")
        if not math.isfinite(smoothing) or smoothing <= 0:
            raise ValueError("smoothing must be positive and finite")
        self.max_order = max_order
        self.smoothing = smoothing
        self.vocabulary: frozenset[Token] = frozenset()
        self._counts: list[dict[tuple[Token, ...], Counter[Token]]] = []
        self._fitted = False

    def fit(self, sequences: Iterable[Sequence[Token]]) -> "VariableOrderExpectancy":
        counts: list[dict[tuple[Token, ...], Counter[Token]]] = [
            defaultdict(Counter) for _ in range(self.max_order + 1)
        ]
        vocabulary: set[Token] = set()
        seen = 0
        for sequence in sequences:
            events = tuple(sequence)
            for pos, event in enumerate(events):
                hash(event)  # Fail clearly for mutable/unhashable symbols.
                if event == "<UNSEEN>":
                    raise ValueError("<UNSEEN> is reserved as the out-of-vocabulary label")
                vocabulary.add(event)
                seen += 1
                for order in range(min(pos, self.max_order) + 1):
                    context = events[pos - order:pos] if order else ()
                    counts[order][context][event] += 1
        if seen == 0:
            raise ValueError("expected at least one training event")
        self.vocabulary = frozenset(vocabulary)
        self._counts = counts
        self._fitted = True
        return self

    def _canonical(self, event: Token) -> Token:
        return event if event in self.vocabulary else _UNSEEN

    def probability(self, event: Token, context: Sequence[Token] = ()) -> float:
        if not self._fitted:
            raise RuntimeError("fit the expectancy model before predicting")
        event = self._canonical(event)
        history = tuple(self._canonical(x) for x in context[-self.max_order:]) if self.max_order else ()
        # Uniform prior allocates nonzero probability to the unseen bucket.
        probability = 1.0 / (len(self.vocabulary) + 1)
        for order in range(self.max_order + 1):
            prefix = history[-order:] if order else ()
            if order > len(history):
                break
            observed = self._counts[order].get(prefix)
            if observed:
                total = sum(observed.values())
                probability = (observed[event] + self.smoothing * probability) / (total + self.smoothing)
        return probability

    def distribution(self, context: Sequence[Token] = ()) -> dict[Token | str, float]:
        if not self._fitted:
            raise RuntimeError("fit the expectancy model before predicting")
        distribution = {x: self.probability(x, context) for x in self.vocabulary}
        distribution["<UNSEEN>"] = self.probability(_UNSEEN, context)
        return distribution

    def entropy(self, context: Sequence[Token] = ()) -> float:
        return -sum(p * math.log2(p) for p in self.distribution(context).values())

    def evaluate(self, sequence: Sequence[Token]) -> list[Expectation]:
        history: list[Token] = []
        result = []
        for pos, event in enumerate(sequence):
            probability = self.probability(event, history)
            result.append(Expectation(
                index=pos, event=str(event), probability=probability,
                surprisal_bits=-math.log2(probability),
                entropy_bits_before=self.entropy(history),
                context_length=min(len(history), self.max_order),
            ))
            history.append(event)
        return result
