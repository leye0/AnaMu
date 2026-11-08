"""Score-to-performance MIDI expression, with a verifiable alignment audit.

For PercePiano only, use the author's paired score MIDI. Equal-pitch note
instances are assigned by minimum time-position cost, independently for each
pitch, using a one-to-one Hungarian matching. This is a deliberately simpler
alignment than the paper's pyScoreParser, and is NOT claimed to replicate it.

All variables come from MIDI. The score supplies relative written timing;
performance MIDI supplies realized onset, duration, and key velocity.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import mido
import numpy as np
from scipy.optimize import linear_sum_assignment


SCORE_FEATURE_NAMES = (
    "rubato_normalized_residual_sd",
    "rubato_local_ratio_sd",
    "rubato_middle_arc",
    "rubato_final_vs_start",
    "rubato_phrase_boundary_relaxation",
    "score_register_dynamic_contrast",
    "score_rhythmic_density_dynamic_coupling",
    "score_velocity_emphasis",
    "articulation_relative_log_median",
    "articulation_relative_log_sd",
    "articulation_short_fraction",
    "articulation_dynamic_correlation",
    "rubato_dynamic_correlation",
    "score_high_note_lead_seconds",
)


def _read_midi(path: Path) -> np.ndarray:
    midi = mido.MidiFile(str(path))
    if midi.type == 2:
        raise ValueError("unsupported_midi_type2")
    seconds, tempo = 0., 500_000
    active = defaultdict(list)
    notes = []
    for msg in mido.merge_tracks(midi.tracks):
        seconds += mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
        if msg.type == "set_tempo":
            tempo = msg.tempo
        elif msg.type in ("note_on", "note_off") and msg.channel != 9:
            key = (msg.channel, msg.note)
            if msg.type == "note_on" and msg.velocity > 0:
                active[key].append((seconds, msg.velocity))
            elif active[key]:
                onset, velocity = active[key].pop(0)
                if seconds > onset:
                    notes.append((float(onset), float(msg.note),
                                  float(seconds - onset), velocity / 127.))
    if len(notes) < 12:
        raise ValueError(f"too_few_valid_notes:{path}")
    notes.sort(key=lambda n: (n[0], n[1]))
    return np.asarray(notes, dtype=float)


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    return (float(np.corrcoef(a, b)[0, 1])
            if len(a) >= 6 and np.std(a) > 1e-9 and np.std(b) > 1e-9 else 0.)


def _score_path(performance_path: Path) -> Path:
    stem = performance_path.stem
    prefix = "_".join(stem.split("_")[:-2])
    if not prefix or len(stem.split("_")) < 5:
        raise ValueError(f"unrecognized_percepiano_stem:{stem}")
    return performance_path.parent.parent / "score_midi" / (
        f"{prefix}_Score_{stem.split('_')[-1]}.mid")


def _aligned_notes(score: np.ndarray, performance: np.ndarray,
                   minimum_coverage: float = .70):
    """One-to-one pitch-class-exact notes; ensure offsets remain monotonic.

    The time cost is determined from normalized duration of the *individual*
    files without access to any emotion rating. Repetitions are disambiguated
    by relative position. This is not score following across transpositions.
    """
    score_range = max(float(np.ptp(score[:, 0])), 1e-3)
    perf_range = max(float(np.ptp(performance[:, 0])), 1e-3)
    score_t = (score[:, 0] - score[0, 0]) / score_range
    perf_t = (performance[:, 0] - performance[0, 0]) / perf_range
    a, b = [], []
    for pitch in np.intersect1d(score[:, 1], performance[:, 1]):
        s_idx = np.flatnonzero(score[:, 1] == pitch)
        p_idx = np.flatnonzero(performance[:, 1] == pitch)
        cost = abs(score_t[s_idx, None] - perf_t[None, p_idx])
        si, pi = linear_sum_assignment(cost)
        a.extend(s_idx[si].tolist())
        b.extend(p_idx[pi].tolist())
    if len(a) < 12:
        raise ValueError("insufficient_pitch_matching")
    a = np.asarray(a, dtype=int)
    b = np.asarray(b, dtype=int)
    # Restrict to reasonable timing correspondences, not just identical keys.
    good = abs(score_t[a] - perf_t[b]) <= .12
    a, b = a[good], b[good]
    if len(a) < 12 or len(a) / min(len(score), len(performance)) < minimum_coverage:
        raise ValueError("unreliable_alignment_coverage")
    order = np.argsort(score[a, 0], kind="stable")
    return a[order], b[order], {
        "match_fraction": len(a) / min(len(score), len(performance)),
        "median_relative_position_error": float(np.median(abs(score_t[a] - perf_t[b]))),
    }


def alignment_quality(performance_path: str | Path) -> dict[str, float]:
    """Read-only audit. Does NOT silently waive the production quality gate."""
    path = Path(performance_path)
    _, _, metrics = _aligned_notes(_read_midi(_score_path(path)),
                                    _read_midi(path), minimum_coverage=0.)
    return metrics


def score_aligned_features(performance_path: str | Path, *,
                           score_notes: np.ndarray | None = None) -> dict[str, float]:
    """Extract 14 descriptors from the matching score and human performance."""
    path = Path(performance_path)
    if score_notes is None:
        score_path = _score_path(path)
        if not score_path.is_file():
            raise FileNotFoundError(score_path)
        score = _read_midi(score_path)
    else:
        score = score_notes
    perf = _read_midi(path)
    a, b, diagnostics = _aligned_notes(score, perf)
    s, p = score[a], perf[b]
    scale = max(float(np.ptp(perf[:, 0]) / max(np.ptp(score[:, 0]), 1e-5)), 1e-5)
    # Fit a global linear tempo map; residuals are deviations from that map,
    # not deviations from arbitrary MIDI tempo tags.
    coeff = np.polyfit(s[:, 0], p[:, 0], deg=1)
    predicted = np.polyval(coeff, s[:, 0])
    residual = (p[:, 0] - predicted) / scale
    score_pos = (s[:, 0] - score[0, 0]) / max(np.ptp(score[:, 0]), 1e-5)
    center = (score_pos >= .25) & (score_pos < .75)
    outer = ~center

    # Distinct written attack positions, to avoid zero score intervals on a
    # chord. The matched performance can arpeggiate an attack, so use median.
    score_onsets = np.unique(s[:, 0])
    s_to_perf = np.asarray([np.median(p[s[:, 0] == onset, 0])
                            for onset in score_onsets])
    score_delta = np.diff(score_onsets)
    performance_delta = np.diff(s_to_perf)
    use = (score_delta > .03) & (performance_delta > .015)
    ratio = np.clip((performance_delta[use] / score_delta[use]) / scale,
                    .2, 5.)
    when = score_onsets[1:][use]
    when_norm = (when - score_onsets[0]) / max(np.ptp(score_onsets), 1e-5)
    early = ratio[when_norm < .25]
    late = ratio[when_norm > .75]
    typical_spacing = float(np.median(score_delta)) if len(score_delta) else 1.
    boundaries = np.flatnonzero(score_delta > typical_spacing * 1.8)
    # Local ratio is attributed to interval ending at a written onset.
    boundary_ending = np.zeros(len(score_delta), dtype=bool)
    boundary_ending[boundaries] = True
    boundary_ratios = boundary_ending[use]
    boundary_relax = (float(np.mean(ratio[boundary_ratios]) -
                            np.mean(ratio[~boundary_ratios]))
                      if np.any(boundary_ratios) and np.any(~boundary_ratios)
                      else 0.)

    articulation = np.log(np.clip(p[:, 2] /
                                  np.maximum(s[:, 2] * scale, .015), .1, 10.))
    # Score identifies simultaneous written notes even if the performance
    # spreads them slightly. High/low register is a proxy for voice, not truth.
    contrast, leads = [], []
    for onset in score_onsets:
        indices = np.flatnonzero(s[:, 0] == onset)
        if len(indices) < 2:
            continue
        high, low = indices[np.argmax(s[indices, 1])], indices[np.argmin(s[indices, 1])]
        if s[high, 1] - s[low, 1] < 4:
            continue
        contrast.append(float(p[high, 3] - p[low, 3]))
        leads.append(float(p[high, 0] - np.median(p[indices[indices != high], 0])))

    # Note density from WRITTEN score, never from the performer/annotation.
    density = np.asarray([np.sum(abs(s[:, 0] - time) <= .25) for time in s[:, 0]],
                         dtype=float)
    expressive_velocity = p[:, 3] - s[:, 3]
    result = {
        "rubato_normalized_residual_sd": float(np.std(residual)),
        "rubato_local_ratio_sd": float(np.std(ratio)) if len(ratio) else 0.,
        "rubato_middle_arc": float(np.mean(residual[center]) - np.mean(residual[outer]))
                               if np.any(center) and np.any(outer) else 0.,
        "rubato_final_vs_start": float(np.mean(late) - np.mean(early))
                                 if len(late) and len(early) else 0.,
        "rubato_phrase_boundary_relaxation": boundary_relax,
        "score_register_dynamic_contrast": float(np.mean(contrast)) if contrast else 0.,
        "score_rhythmic_density_dynamic_coupling": _corr(density, expressive_velocity),
        "score_velocity_emphasis": float(np.std(expressive_velocity)),
        "articulation_relative_log_median": float(np.median(articulation)),
        "articulation_relative_log_sd": float(np.std(articulation)),
        "articulation_short_fraction": float(np.mean(articulation < np.log(.65))),
        "articulation_dynamic_correlation": _corr(articulation, expressive_velocity),
        "rubato_dynamic_correlation": _corr(residual, expressive_velocity),
        "score_high_note_lead_seconds": float(np.mean(leads)) if leads else 0.,
    }
    if not all(np.isfinite(value) for value in result.values()):
        raise ValueError("nonfinite_aligned_features")
    # Diagnostics are kept out of the learning features, to prevent using
    # transcription/alignment quality as a shortcut for perceived emotion.
    result["alignment_diagnostics"] = diagnostics
    return result
