"""
EQ parameter calculator for NIO Pro EQ.

Pipeline:
  1. Build a Harman-style automotive target curve
  2. Compute the error curve  (target − measured)
  3. Detect the 7 most significant peaks/valleys in the error curve
  4. Assign filter type (Low Shelf / High Shelf / Bell) and estimate Q
  5. Return a list of 7 EQFilter objects
"""
from __future__ import annotations

from typing import List, Tuple

import numpy as np
from scipy.signal import find_peaks

from app.core.config import settings
from app.models.schemas import (
    FrequencyPoint,
    EQFilter,
    FilterType,
)

# ── Harman Automotive Target Curve ──────────────────────────────────
#
# Piecewise-linear definition in (frequency_Hz, gain_dB) anchors.
# Based on Harman's published in-car preference research:
#   • Sub-bass shelf:  gentle +3 … +6 dB below 80 Hz
#   • Bass rolloff:    gradual return to 0 dB by ~200 Hz
#   • Midrange:        flat reference  200 – 2000 Hz
#   • Presence dip:    slight -1 dB around 2 – 4 kHz
#   • Treble rolloff:  smooth descent to -8 dB at 20 kHz
#
_TARGET_ANCHORS: List[Tuple[float, float]] = [
    (20,    6.0),
    (40,    5.5),
    (63,    4.5),
    (80,    3.5),
    (125,   1.5),
    (200,   0.0),
    (500,   0.0),
    (1000,  0.0),
    (2000, -0.5),
    (3150, -1.5),
    (4000, -2.5),
    (5000, -3.5),
    (6300, -4.5),
    (8000, -5.5),
    (10000, -6.5),
    (12500, -7.0),
    (16000, -7.5),
    (20000, -8.0),
]

# Boundaries (Hz) below which → Low Shelf, above which → High Shelf
_LOW_SHELF_CEILING = 120.0
_HIGH_SHELF_FLOOR = 8000.0

# Minimum separation between two chosen EQ nodes (in octaves)
_MIN_OCTAVE_SEPARATION = 0.45


class EQCalculator:
    """Analyzes deviation from the Harman target and produces 7 parametric EQ filters."""

    # ── public ──────────────────────────────────────────────────────

    def calculate(
        self,
        measured: list[FrequencyPoint],
    ) -> tuple[list[FrequencyPoint], list[FrequencyPoint], list[EQFilter], float, str]:
        """
        Returns
        -------
        (target_curve, error_curve, eq_filters, score, summary)
        """
        freqs = np.array([p.frequency for p in measured])
        measured_db = np.array([p.magnitude_db for p in measured])

        target_db = self._interpolate_target(freqs)

        # Align measured curve to target in the 200–2000 Hz mid-range reference band.
        # The measured curve is normalized to peak=0 dB internally, so we shift it
        # so its mid-range average matches the target's mid-range average.
        mid_mask = (freqs >= 200) & (freqs <= 2000)
        if np.any(mid_mask):
            offset = np.mean(target_db[mid_mask]) - np.mean(measured_db[mid_mask])
            measured_db = measured_db + offset

        error_db = target_db - measured_db  # positive = need boost, negative = need cut

        target_points = [
            FrequencyPoint(frequency=float(f), magnitude_db=round(float(t), 2))
            for f, t in zip(freqs, target_db)
        ]
        error_points = [
            FrequencyPoint(frequency=float(f), magnitude_db=round(float(e), 2))
            for f, e in zip(freqs, error_db)
        ]

        filters = self._find_eq_filters(freqs, error_db)

        score = self._compute_score(error_db)
        summary = self._generate_summary(score, filters)

        return target_points, error_points, filters, score, summary

    # ── target curve interpolation ──────────────────────────────────

    @staticmethod
    def _interpolate_target(freqs: np.ndarray) -> np.ndarray:
        """Log-frequency linear interpolation of the Harman target anchors."""
        anchor_f = np.array([a[0] for a in _TARGET_ANCHORS])
        anchor_db = np.array([a[1] for a in _TARGET_ANCHORS])
        return np.interp(np.log10(freqs), np.log10(anchor_f), anchor_db)

    # ── peak / valley detection + EQ assignment ─────────────────────

    def _find_eq_filters(
        self,
        freqs: np.ndarray,
        error_db: np.ndarray,
    ) -> list[EQFilter]:
        n_filters = settings.EQ_FILTER_COUNT
        gain_min = settings.EQ_GAIN_MIN
        gain_max = settings.EQ_GAIN_MAX

        candidates = self._detect_candidates(freqs, error_db)

        if not candidates:
            return self._fallback_uniform(freqs, error_db, n_filters)

        selected = self._select_top_n(candidates, n_filters)

        filters: list[EQFilter] = []
        for freq_hz, gain_raw, q_est in selected:
            gain = float(np.clip(gain_raw, gain_min, gain_max))
            gain = round(gain * 2) / 2  # snap to 0.5 dB
            if abs(gain) < 0.5:
                continue

            q = float(np.clip(q_est, settings.EQ_Q_MIN, settings.EQ_Q_MAX))
            q = round(q * 10) / 10

            ftype = self._choose_filter_type(freq_hz)
            freq_int = int(round(freq_hz))
            freq_int = max(20, min(20000, freq_int))

            filters.append(EQFilter(
                type=ftype,
                frequency=freq_int,
                gain=round(gain, 1),
                q_factor=round(q, 1),
            ))

        # pad to exactly n_filters if we didn't get enough
        while len(filters) < n_filters:
            extras = self._fallback_uniform(freqs, error_db, n_filters - len(filters))
            used_freqs = {f.frequency for f in filters}
            added = False
            for ef in extras:
                if ef.frequency not in used_freqs:
                    filters.append(ef)
                    added = True
                if len(filters) >= n_filters:
                    break
            if not added:
                # avoid infinite loop: accept duplicates with shifted frequency
                for ef in extras:
                    ef_shifted = EQFilter(
                        type=ef.type,
                        frequency=min(20000, ef.frequency + 1),
                        gain=ef.gain,
                        q_factor=ef.q_factor,
                    )
                    filters.append(ef_shifted)
                    if len(filters) >= n_filters:
                        break

        filters.sort(key=lambda f: f.frequency)
        return filters[:n_filters]

    def _detect_candidates(
        self,
        freqs: np.ndarray,
        error_db: np.ndarray,
    ) -> list[tuple[float, float, float]]:
        """
        Find peaks (need boost) and valleys (need cut) in the error curve.

        Returns list of (frequency_hz, gain_db, estimated_Q).
        """
        candidates: list[tuple[float, float, float]] = []
        abs_error = np.abs(error_db)

        # Peaks in error curve → frequencies that need boost
        peak_idx, peak_props = find_peaks(
            error_db, height=1.0, distance=2, prominence=0.8
        )
        for idx in peak_idx:
            q = self._estimate_q(freqs, error_db, idx)
            candidates.append((float(freqs[idx]), float(error_db[idx]), q))

        # Peaks in inverted error → frequencies that need cut
        valley_idx, valley_props = find_peaks(
            -error_db, height=1.0, distance=2, prominence=0.8
        )
        for idx in valley_idx:
            q = self._estimate_q(freqs, -error_db, idx)
            candidates.append((float(freqs[idx]), float(error_db[idx]), q))

        # Sort by absolute magnitude (most severe first)
        candidates.sort(key=lambda c: abs(c[1]), reverse=True)
        return candidates

    @staticmethod
    def _estimate_q(
        freqs: np.ndarray,
        curve: np.ndarray,
        peak_idx: int,
    ) -> float:
        """
        Estimate Q from the -3 dB bandwidth of a peak.

        Q = f_center / bandwidth
        """
        peak_val = curve[peak_idx]
        threshold = peak_val - 3.0
        fc = freqs[peak_idx]

        # walk left to find -3 dB crossing
        f_lo = fc
        for i in range(peak_idx - 1, -1, -1):
            if curve[i] <= threshold:
                # linear interpolation
                frac = (threshold - curve[i]) / (curve[i + 1] - curve[i] + 1e-12)
                f_lo = freqs[i] + frac * (freqs[i + 1] - freqs[i])
                break

        # walk right
        f_hi = fc
        for i in range(peak_idx + 1, len(curve)):
            if curve[i] <= threshold:
                frac = (threshold - curve[i]) / (curve[i - 1] - curve[i] + 1e-12)
                f_hi = freqs[i] - frac * (freqs[i] - freqs[i - 1])
                break

        bandwidth = f_hi - f_lo
        if bandwidth <= 0:
            return 4.0  # narrow peak default

        q = fc / bandwidth
        return max(0.5, min(10.0, q))

    def _select_top_n(
        self,
        candidates: list[tuple[float, float, float]],
        n: int,
    ) -> list[tuple[float, float, float]]:
        """
        Greedily pick the top-N candidates while maintaining minimum
        octave separation between chosen nodes.
        """
        selected: list[tuple[float, float, float]] = []
        for cand in candidates:
            if len(selected) >= n:
                break
            freq = cand[0]
            too_close = any(
                abs(np.log2(freq / s[0])) < _MIN_OCTAVE_SEPARATION
                for s in selected
            )
            if not too_close:
                selected.append(cand)
        return selected

    @staticmethod
    def _choose_filter_type(freq_hz: float) -> FilterType:
        if freq_hz <= _LOW_SHELF_CEILING:
            return FilterType.LOW_SHELF
        if freq_hz >= _HIGH_SHELF_FLOOR:
            return FilterType.HIGH_SHELF
        return FilterType.BELL

    # ── fallback: uniform sampling across log-frequency ─────────────

    def _fallback_uniform(
        self,
        freqs: np.ndarray,
        error_db: np.ndarray,
        n: int,
    ) -> list[EQFilter]:
        """When peak detection yields too few results, sample uniformly."""
        log_f = np.log10(freqs)
        sample_points = np.linspace(log_f[0], log_f[-1], n + 2)[1:-1]
        filters: list[EQFilter] = []

        for lf in sample_points:
            idx = int(np.argmin(np.abs(log_f - lf)))
            freq_hz = float(freqs[idx])
            gain = float(np.clip(error_db[idx], settings.EQ_GAIN_MIN, settings.EQ_GAIN_MAX))
            gain = round(gain * 2) / 2
            if abs(gain) < 0.5:
                gain = 0.5 if error_db[idx] > 0 else -0.5

            filters.append(EQFilter(
                type=self._choose_filter_type(freq_hz),
                frequency=max(20, min(20000, int(round(freq_hz)))),
                gain=round(gain, 1),
                q_factor=2.0,
            ))

        return filters

    # ── scoring & summary ───────────────────────────────────────────

    @staticmethod
    def _compute_score(error_db: np.ndarray) -> float:
        """
        Score based on RMS error across all 1/3-octave bands.
        0 dB RMS error → 100 points;  ≥10 dB RMS → 0 points.
        """
        rms = float(np.sqrt(np.mean(error_db ** 2)))
        score = max(0.0, min(100.0, 100.0 - rms * 10.0))
        return round(score, 1)

    @staticmethod
    def _generate_summary(score: float, filters: list[EQFilter]) -> str:
        boosts = [f for f in filters if f.gain >= 1.5]
        cuts = [f for f in filters if f.gain <= -1.5]

        parts = [f"综合评分 {score:.0f}/100。"]

        if boosts:
            freqs = "、".join(f"{f.frequency}Hz" for f in boosts)
            parts.append(f"建议提升频段：{freqs}。")
        if cuts:
            freqs = "、".join(f"{f.frequency}Hz" for f in cuts)
            parts.append(f"建议衰减频段：{freqs}。")
        if not boosts and not cuts:
            parts.append("车内频响已较为平坦，无需大幅调整。")

        return " ".join(parts)
