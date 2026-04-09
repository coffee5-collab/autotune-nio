"""
Audio frequency-response analysis with 1/3-octave smoothing.

Pipeline:
  raw audio bytes → decode → mono → resample → STFT → magnitude spectrum
  → 1/3-octave band averaging → dB conversion → FrequencyPoint list
"""
from __future__ import annotations

import io
import subprocess
import tempfile
from typing import List, Tuple

import numpy as np
import librosa
import soundfile as sf

from app.core.config import settings
from app.models.schemas import FrequencyPoint

# ISO 266 standard 1/3-octave center frequencies (20 Hz – 20 kHz)
THIRD_OCTAVE_CENTERS: np.ndarray = np.array([
    20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160,
    200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
    2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000,
])

# 1/3-octave bandwidth factor: each band spans center / 2^(1/6) to center * 2^(1/6)
_BANDWIDTH_FACTOR = 2 ** (1.0 / 6.0)


class AudioAnalyzer:
    """Reads uploaded audio and returns a 1/3-octave smoothed frequency response."""

    def __init__(
        self,
        sample_rate: int = settings.SAMPLE_RATE,
        n_fft: int = settings.FFT_SIZE,
        hop_length: int = settings.HOP_LENGTH,
    ):
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length

    # ── public ──────────────────────────────────────────────────────

    def analyze(self, audio_bytes: bytes) -> Tuple[List[FrequencyPoint], int, float]:
        """
        Returns
        -------
        (smoothed_points, sample_rate, duration_seconds)
        """
        y, sr = self._load(audio_bytes)
        duration = float(len(y) / sr)

        freqs, magnitude = self._compute_spectrum(y, sr)
        smoothed = self._smooth_third_octave(freqs, magnitude)

        return smoothed, sr, duration

    # ── private ─────────────────────────────────────────────────────

    def _load(self, raw: bytes) -> Tuple[np.ndarray, int]:
        try:
            y, sr = sf.read(io.BytesIO(raw), dtype="float64")
        except Exception:
            y, sr = self._load_via_ffmpeg(raw)

        if y.ndim > 1:
            y = np.mean(y, axis=1)

        if sr != self.sample_rate:
            y = librosa.resample(y, orig_sr=sr, target_sr=self.sample_rate)
            sr = self.sample_rate

        return y, sr

    @staticmethod
    def _load_via_ffmpeg(raw: bytes) -> Tuple[np.ndarray, int]:
        """Fallback: convert webm/ogg/etc. to WAV via ffmpeg, then read."""
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_in:
            tmp_in.write(raw)
            tmp_in.flush()
            tmp_out = tmp_in.name.replace(".webm", ".wav")
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_in.name, "-ar", "48000", "-ac", "1", tmp_out],
                capture_output=True,
                check=True,
            )
        y, sr = sf.read(tmp_out, dtype="float64")
        return y, sr

    def _compute_spectrum(
        self, y: np.ndarray, sr: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Time-averaged magnitude spectrum (linear)."""
        S = np.abs(librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length))
        avg_magnitude = np.mean(S, axis=1)  # average across all time frames
        freqs = librosa.fft_frequencies(sr=sr, n_fft=self.n_fft)
        return freqs, avg_magnitude

    def _smooth_third_octave(
        self,
        freqs: np.ndarray,
        magnitude: np.ndarray,
    ) -> List[FrequencyPoint]:
        """
        Aggregate FFT bins into 1/3-octave bands.

        For each ISO center frequency, average all FFT bins whose frequency
        falls within [center / 2^(1/6),  center * 2^(1/6)].
        """
        # keep only centers below Nyquist
        nyquist = self.sample_rate / 2.0
        centers = THIRD_OCTAVE_CENTERS[THIRD_OCTAVE_CENTERS <= nyquist]

        points: list[FrequencyPoint] = []
        ref = np.max(magnitude) if np.max(magnitude) > 0 else 1.0

        for fc in centers:
            f_lo = fc / _BANDWIDTH_FACTOR
            f_hi = fc * _BANDWIDTH_FACTOR
            mask = (freqs >= f_lo) & (freqs <= f_hi)

            if np.any(mask):
                band_avg = np.mean(magnitude[mask])
            else:
                # fallback: nearest bin
                idx = np.argmin(np.abs(freqs - fc))
                band_avg = magnitude[idx]

            db = 20.0 * np.log10(band_avg / ref + 1e-12)
            points.append(FrequencyPoint(
                frequency=float(fc),
                magnitude_db=round(float(db), 2),
            ))

        return points
