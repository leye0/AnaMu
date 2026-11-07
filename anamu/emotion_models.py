"""Separate between-piece mood from within-piece emotional movement.

This is a deterministic, grouped hierarchical regression baseline. It does
not assign emotions by musical rules; as with other regressors, human labels
from training compositions supervise the mapping. The feature extractor
never sees labels and the split is composition-disjoint.
"""

from __future__ import annotations

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler


def _ranges(lengths):
    start = 0
    for span in lengths:
        if span <= 0:
            raise ValueError("empty_piece_in_temporal_model")
        yield slice(start, start + span)
        start += span


class GroupedTemporalRegressor:
    """Two independent shrinkage scales for global mood and musical change."""

    def __init__(self, *, global_alpha: float = 100., local_alpha: float = 100.):
        self.global_alpha = global_alpha
        self.local_alpha = local_alpha
        self.imputer = SimpleImputer(strategy="median", keep_empty_features=True)
        self.scaler = StandardScaler()
        self.global_model = Ridge(alpha=global_alpha, solver="lsqr")
        self.local_model = Ridge(alpha=local_alpha, solver="lsqr")
        self.fitted = False

    def _prepare(self, matrix, *, training=False):
        matrix = np.asarray(matrix, dtype=float)
        if matrix.ndim != 2:
            raise ValueError("expected_flat_feature_matrix")
        if training:
            matrix = self.imputer.fit_transform(matrix)
            return self.scaler.fit_transform(matrix)
        return self.scaler.transform(self.imputer.transform(matrix))

    @staticmethod
    def _decompose(matrix, lengths):
        spans = list(_ranges(lengths))
        if spans[-1].stop != len(matrix):
            raise ValueError("piece_lengths_do_not_match_rows")
        means = np.stack([matrix[span].mean(axis=0) for span in spans])
        centered = matrix - np.concatenate([
            np.broadcast_to(mean, (span.stop - span.start, len(mean)))
            for span, mean in zip(spans, means)])
        return means, centered, spans

    def fit(self, matrix, targets, lengths):
        features = self._prepare(matrix, training=True)
        targets = np.asarray(targets, dtype=float)
        if targets.shape != (len(features), 2):
            raise ValueError("emotion_targets_must_be_two_columns")
        piece_means, residual_features, spans = self._decompose(features, lengths)
        emotion_means = np.stack([targets[span].mean(axis=0) for span in spans])
        residual_targets = targets - np.concatenate([
            np.broadcast_to(mean, (span.stop - span.start, 2))
            for span, mean in zip(spans, emotion_means)])
        weights = np.concatenate([
            np.full(span.stop - span.start, 1 / (span.stop - span.start))
            for span in spans])
        self.global_model.fit(piece_means, emotion_means)
        self.local_model.fit(residual_features, residual_targets, sample_weight=weights)
        self.fitted = True
        return self

    def predict(self, matrix, lengths):
        if not self.fitted:
            raise RuntimeError("fit_temporal_model_before_predict")
        features = self._prepare(matrix)
        piece_means, residual_features, spans = self._decompose(features, lengths)
        global_emotions = self.global_model.predict(piece_means)
        global_at_row = np.concatenate([
            np.broadcast_to(mean, (span.stop - span.start, 2))
            for span, mean in zip(spans, global_emotions)])
        return np.clip(global_at_row + self.local_model.predict(residual_features), -1, 1)
