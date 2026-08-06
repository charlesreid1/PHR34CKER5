"""
Tests for the typed-record KR layer: the store, the load-time contract, and
the retrieval tools — including the adversarial trap catalog that separates
this from a Wikipedia paraphrase.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from phr34cker5_mcp import records, server

RECORDS_DIR = Path(__file__).resolve().parents[1] / "knowledge" / "records"


@pytest.fixture(scope="module")
def store():
    return records.RecordStore.load(RECORDS_DIR)


# --- load-time contract ------------------------------------------------------


def test_store_loads(store):
    assert len(store.records) > 30
    assert store.by_category["tone_signal"]
    assert store.by_category["bibliography"]


def test_every_nonbib_record_has_resolvable_citations(store):
    bib_ids = {r["id"] for r in store.in_category("bibliography")}
    for rec in store.all_records():
        if rec.get("category") == "bibliography":
            continue
        cites = rec.get("citations") or []
        assert cites, f"{rec['id']} has empty citations"
        assert all(c in bib_ids for c in cites), f"{rec['id']} cites unknown source"


def test_every_record_has_two_element_era_bounds(store):
    for rec in store.all_records():
        if rec.get("category") == "bibliography":
            continue
        eb = rec.get("era_bounds")
        assert isinstance(eb, list) and len(eb) == 2, f"{rec['id']} era_bounds"


def test_empty_citations_raises(tmp_path):
    (tmp_path / "bibliography.json").write_text('[{"id":"b1","category":"bibliography"}]')
    (tmp_path / "tones.json").write_text(
        '[{"id":"t1","category":"tone_signal","era_bounds":[null,null],"citations":[]}]'
    )
    with pytest.raises(records.RecordError, match="empty citations"):
        records.RecordStore.load(tmp_path)


def test_unresolved_citation_raises(tmp_path):
    (tmp_path / "bibliography.json").write_text('[{"id":"b1","category":"bibliography"}]')
    (tmp_path / "tones.json").write_text(
        '[{"id":"t1","category":"tone_signal","era_bounds":[null,null],"citations":["nope"]}]'
    )
    with pytest.raises(records.RecordError, match="does not resolve"):
        records.RecordStore.load(tmp_path)


def test_duplicate_id_raises(tmp_path):
    (tmp_path / "bibliography.json").write_text(
        '[{"id":"b1","category":"bibliography"},{"id":"b1","category":"bibliography"}]'
    )
    with pytest.raises(records.RecordError, match="duplicate"):
        records.RecordStore.load(tmp_path)


# --- resolution + era --------------------------------------------------------


def test_alias_resolution(store):
    assert store.resolve("2600")["id"] == "sf_2600"
    assert store.resolve("the whistle")["id"] == "sf_2600"
    assert store.resolve("red box quarter")["id"] == "acts_quarter"
    assert store.resolve("KP")["id"] == "mf_kp"


def test_era_contains(store):
    bluebox = store.get("technique_blue_box_domestic")
    assert records.era_contains(bluebox, 1975)
    assert not records.era_contains(bluebox, 2005)


def test_open_ended_era(store):
    dtmf = store.get("dtmf_1")  # era_bounds last = null
    assert records.era_contains(dtmf, 2026)


# --- lookup_tone -------------------------------------------------------------


def test_lookup_tone_quarter_timing(store):
    r = server.lookup_tone("acts_quarter")
    assert r["technical_body"]["on_ms"] == 33
    assert "timing" in r["disputed"]
    assert r["technical_body"]["frequencies_hz"] == [1700, 2200]


def test_lookup_tone_by_alias(store):
    assert server.lookup_tone("the whistle")["id"] == "sf_2600"


def test_lookup_tone_unknown_raises(store):
    with pytest.raises(ValueError, match="no tone record"):
        server.lookup_tone("purple box hum")


# --- verify_claim: the adversarial traps -------------------------------------


def test_trap_2600_international_is_false(store):
    v = server.verify_claim("a blue box uses 2600 Hz to hang up an international trunk")
    assert v["verdict"] == "false"
    assert any(rec["id"] == "ccitt5_line_seize" for rec in v["records"])


def test_trap_quarter_66ms_is_false(store):
    v = server.verify_claim("the ACTS quarter tone is five 66 ms bursts")
    assert v["verdict"] == "false"


def test_trap_universal_anac_needs_qualification(store):
    v = server.verify_claim("the ANAC is 958")
    assert v["verdict"] == "needs_qualification"


def test_trap_kp2_naming_needs_qualification(store):
    v = server.verify_claim("KP2 is 700+1700 Hz")
    assert v["verdict"] == "needs_qualification"


def test_trap_autovon_d_flash_override_is_false(store):
    v = server.verify_claim("in AUTOVON, D means Flash Override")
    assert v["verdict"] == "false"


def test_unmatched_claim_is_unverified_not_bluffed(store):
    v = server.verify_claim("the sky is blue")
    assert v["verdict"] == "unverified"
    assert v["records"] == []


# --- explain_technique -------------------------------------------------------


def test_explain_technique_never_refuses_out_of_era(store):
    # A phreaking CTF is exactly where old techniques get used. Always return
    # the steps; the out-of-era case only adds a non-blocking context note.
    e = server.explain_technique("blueboxing", year=2005)
    assert e["steps"]
    assert "applicable" not in e and "refusals" not in e
    assert e["context_notes"]  # heads-up, not a gate


def test_explain_technique_in_era_has_no_note(store):
    e = server.explain_technique("redboxing", year=1993)
    assert e["steps"]
    assert e["context_notes"] == []


def test_explain_technique_wrong_region_still_returns_steps(store):
    e = server.explain_technique("blueboxing", region="ITU-R2")
    assert e["steps"]
    assert e["context_notes"]


def test_explain_technique_no_args_no_notes(store):
    e = server.explain_technique("blueboxing")
    assert e["steps"]
    assert e["context_notes"] == []


# --- bibliography / cross_reference / search_records -------------------------


def test_bibliography_lookup(store):
    b = server.bibliography("gr-506-core")
    assert "GR-506-CORE" in b["title"]


def test_bibliography_list(store):
    assert len(server.bibliography()["sources"]) >= 5


def test_cross_reference(store):
    x = server.cross_reference("box_red")
    assert x["id"] == "box_red"
    assert any(l["id"] == "acts_quarter" and l["resolved"] for l in x["see_also"])


def test_search_records_by_region_and_year(store):
    s = server.search_records(category="tone_signal", region="NANP", year=1998)
    assert s["hit_count"] > 0
    # a No.5 international tone must NOT appear in an NANP filter
    assert all(r["region"] == "NANP" for r in s["results"])


def test_search_records_query(store):
    s = server.search_records(query="fax")
    ids = {r["id"] for r in s["results"]}
    assert {"fax_cng", "fax_ced"} <= ids
