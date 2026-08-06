"""
Tests for scripts/generate-tone-fixtures.py.

Runs the generator into a temp directory so we don't depend on the
committed checksums file matching (that check has its own --verify path).
Confirms every renderable tone_signal record produces a WAV whose
duration matches technical_body.on_ms, and that the render is
deterministic across two consecutive runs.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import wave
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPO_ROOT / "scripts" / "generate-tone-fixtures.py"
TONES_JSON = REPO_ROOT / "knowledge" / "records" / "tones.json"


@pytest.fixture(scope="module")
def generator():
    """Load the generator as a module (its filename has a hyphen)."""
    spec = importlib.util.spec_from_file_location("tone_fixture_generator", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def rendered(tmp_path_factory, generator):
    """Render fixtures once per module. Returns (out_dir, {name: sha256})."""
    out = tmp_path_factory.mktemp("tone-fixtures")
    checksums = generator.render_all(out)
    return out, checksums


@pytest.fixture(scope="module")
def tone_records():
    return json.loads(TONES_JSON.read_text())


def test_generator_emits_a_file_per_renderable_record(rendered, tone_records):
    _, checksums = rendered
    # Every single-freq or two-freq record should have a corresponding WAV.
    renderable_ids = {
        r["id"] for r in tone_records
        if r.get("technical_body", {}).get("frequencies_hz")
        and len(r["technical_body"]["frequencies_hz"]) in (1, 2)
    }
    got_ids = {name[:-4] for name in checksums}  # strip .wav
    assert renderable_ids == got_ids, (
        f"missing: {renderable_ids - got_ids}, extra: {got_ids - renderable_ids}"
    )


def test_generator_skips_records_with_no_frequencies(rendered, tone_records, generator):
    """Records without renderable technical_body must yield None, not an empty WAV."""
    for rec in tone_records:
        tb = rec.get("technical_body") or {}
        freqs = tb.get("frequencies_hz") or []
        if not freqs or len(freqs) > 2:
            assert generator.render_record(rec) is None, (
                f"{rec['id']}: expected None but got PCM"
            )


def test_wav_duration_matches_record(rendered, tone_records, generator):
    """Each WAV's frame count should equal the record's on_ms (or fallback) in samples."""
    out_dir, _ = rendered
    for rec in tone_records:
        tb = rec.get("technical_body") or {}
        freqs = tb.get("frequencies_hz") or []
        if not freqs or len(freqs) > 2:
            continue
        expected_ms = tb.get("on_ms") or generator.FALLBACK_MS
        wav_path = out_dir / f"{rec['id']}.wav"
        assert wav_path.exists(), f"missing WAV for {rec['id']}"
        with wave.open(str(wav_path), "rb") as w:
            frames = w.getnframes()
            rate = w.getframerate()
            assert rate == 8000, f"{rec['id']}: sample rate must be 8000 Hz"
            actual_ms = frames * 1000 // rate
            # Allow 1 ms tolerance for rounding.
            assert abs(actual_ms - expected_ms) <= 1, (
                f"{rec['id']}: expected {expected_ms} ms, got {actual_ms} ms"
            )


def test_render_is_deterministic(tmp_path, generator):
    """Two consecutive renders into different dirs must produce identical bytes."""
    a = tmp_path / "a"
    b = tmp_path / "b"
    ca = generator.render_all(a)
    cb = generator.render_all(b)
    assert ca == cb, "renderer is non-deterministic"


def test_committed_checksums_match_current_render(rendered, generator):
    """The committed tests/fixtures/tones.sha256 must match a fresh render.

    If this fails after a records/ edit, run:
        python scripts/generate-tone-fixtures.py
    to regenerate the checksums, and review the diff.
    """
    checksum_path = REPO_ROOT / "tests" / "fixtures" / "tones.sha256"
    if not checksum_path.exists():
        pytest.skip("no committed checksum file — run the generator once to create it")
    _, checksums = rendered
    committed = generator.parse_checksum_file(checksum_path.read_text())
    assert committed == checksums, (
        "committed checksums drift from current render — "
        "run scripts/generate-tone-fixtures.py to update them"
    )


def test_generator_write_and_verify_roundtrip(tmp_path, generator, monkeypatch):
    """Running the generator, then --verify, in the same directory must succeed."""
    # Patch the module-level paths so we don't clobber the real committed file.
    out = tmp_path / "out"
    checksums_path = tmp_path / "tones.sha256"
    monkeypatch.setattr(generator, "DEFAULT_OUT", out)
    monkeypatch.setattr(generator, "CHECKSUM_PATH", checksums_path)

    # First run: write.
    monkeypatch.setattr("sys.argv", ["generate-tone-fixtures.py", "--out", str(out)])
    assert generator.main() == 0
    assert checksums_path.exists()

    # Second run in --verify mode.
    monkeypatch.setattr("sys.argv", ["generate-tone-fixtures.py", "--out", str(out), "--verify"])
    assert generator.main() == 0
