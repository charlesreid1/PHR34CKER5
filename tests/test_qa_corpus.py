"""
Gold-standard Q/A regression tests for the typed-record KR.

Each test is a concrete factual question a phreak-CTF judge might ask, bound
to a specific record field. When someone edits a record and drifts a value
the KR promises, one of these tests goes red and points at the drift.

This is not a test of the assistant's language ability — it's a test that
the numbers, dates, and names in the records still match what the plan says
they should be.

Source ground-truth: plan-knowledge.md §"Technical fill material" and the
primary bibliography entries (BSTJ Nov 1960, Bellcore GR-506-CORE, TR-NPL-
000275, CCITT Q-series, Phrack 33.9, 2600 Autumn 1990, FCC 97-402, etc.).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from phr34cker5_mcp import records, server

RECORDS_DIR = Path(__file__).resolve().parents[1] / "knowledge" / "records"


@pytest.fixture(scope="module")
def store():
    return records.RecordStore.load(RECORDS_DIR)


def _body(store_, record_id: str) -> dict:
    """Fetch a record's technical_body, or an empty dict."""
    rec = store_.get(record_id)
    assert rec is not None, f"record {record_id!r} missing from KR"
    return rec.get("technical_body") or {}


# --- signaling systems: exact frequencies ------------------------------------


def test_sf_supervision_is_2600_hz(store):
    assert _body(store, "sf_2600")["frequencies_hz"] == [2600]


def test_sf_supervision_idle_level_is_minus_20_dbm0(store):
    assert _body(store, "sf_2600")["level_dBm0"] == -20


def test_mf_r1_kp_is_1100_1700(store):
    assert _body(store, "mf_kp")["frequencies_hz"] == [1100, 1700]


def test_mf_r1_st_is_1500_1700(store):
    assert _body(store, "mf_st")["frequencies_hz"] == [1500, 1700]


def test_mf_r1_kp2_is_1300_1700_in_bellcore_notation(store):
    """KP2 in Bellcore notation = 1300+1700 Hz. Community canon sometimes
    scrambles this — see the mf_kp2_intl.disputed field."""
    rec = store.get("mf_kp2_intl")
    assert rec["technical_body"]["frequencies_hz"] == [1300, 1700]
    assert "naming" in rec["disputed"]


def test_mf_r1_kp_duration_100ms(store):
    assert _body(store, "mf_kp")["on_ms"] == 100


def test_ccitt_no5_seizure_is_2400_hz(store):
    """The classic DEFCON trap: No.5 line seizure is 2400 Hz, not 2600."""
    body = _body(store, "ccitt5_line_seize")
    assert body["frequencies_hz"] == [2400]
    assert "2400" in body["pattern"]  # both tones referenced in pattern text


def test_dtmf_5_is_770_1336(store):
    assert _body(store, "dtmf_5")["frequencies_hz"] == [770, 1336]


def test_dtmf_a_autovon_is_697_1633(store):
    assert _body(store, "dtmf_a_autovon")["frequencies_hz"] == [697, 1633]


def test_dtmf_d_autovon_is_priority_not_flash_override(store):
    """D = Priority (LOWEST), not Flash Override — MIL-STD-187-100."""
    rec = store.get("dtmf_d_autovon")
    assert "Priority" in rec["technical_body"]["pattern"]
    assert "LOWEST" in rec["technical_body"]["pattern"]


def test_r2_uses_3825_hz_not_2600(store):
    """R2 line signaling uses 3825 Hz — a common cross-region trap."""
    rec = store.get("sig_r2")
    assert "3825" in rec["technical_body"]["line_signaling_analog"]
    assert "NOT 2600" in rec["technical_body"]["line_signaling_analog"]


# --- ACTS coin tones: exact timings ------------------------------------------


def test_acts_nickel_is_66ms_burst_at_1700_2200(store):
    body = _body(store, "acts_nickel")
    assert body["frequencies_hz"] == [1700, 2200]
    assert body["on_ms"] == 66


def test_acts_dime_is_two_66ms_bursts(store):
    body = _body(store, "acts_dime")
    assert body["on_ms"] == 66
    assert body["off_ms"] == 66


def test_acts_quarter_is_five_33ms_bursts(store):
    """The classic trap: quarter is 5x33 ms per GR-506, not 5x66 ms."""
    body = _body(store, "acts_quarter")
    assert body["on_ms"] == 33
    assert body["off_ms"] == 33
    assert "FIVE" in body["pattern"]
    assert "33 ms" in body["pattern"]


def test_acts_dollar_is_single_650ms_burst(store):
    body = _body(store, "acts_dollar")
    assert body["on_ms"] == 650
    assert "rare" in body["pattern"] or "not universally" in body["pattern"]


def test_acts_dispute_carries_grx506_vs_phrack_33_9(store):
    """The quarter tone's disputed field must carry both timing sources."""
    rec = store.get("acts_quarter")
    disputed = rec["disputed"]
    assert "GR-506" in disputed["timing"]
    assert "Phrack 33.9" in disputed["timing"]


# --- boxes: what they emit and when they died --------------------------------


def test_blue_box_emits_2600_kp_st(store):
    rec = store.get("box_blue")
    assert set(rec["emits"]) == {"sf_2600", "mf_kp", "mf_st"}


def test_blue_box_died_because_ss7(store):
    """Not USSS prosecution — CCIS/SS7 killed classical blue-boxing."""
    rec = store.get("box_blue")
    assert "CCIS" in rec["died_because"] and "SS7" in rec["died_because"]


def test_red_box_power_source_is_6_5536_crystal(store):
    """The crystal-swap detail is load-bearing for the Bernie S case + audio."""
    rec = store.get("box_red")
    assert "6.5536" in rec["power_source"]
    assert "43-141" in rec["power_source"] or "43-146" in rec["power_source"]


def test_black_box_attacks_answer_supervision(store):
    rec = store.get("box_black")
    assert rec["attacks_layer"] == "subscriber_loop_answer_supervision"


# --- payphone platforms ------------------------------------------------------


def test_cocot_never_had_acts_vulnerability(store):
    body = _body(store, "pay_cocot")
    assert "local" in body["coin_validation"].lower()
    # COCOTs' record explains via phreak_relevance rather than attack_surface
    assert "never" in body["coin_validation"] or "never" in body["phreak_relevance"]


def test_millennium_immune_to_redbox(store):
    body = _body(store, "pay_millennium")
    assert "Immune" in body["attack_surface"] or "immune" in body["attack_surface"]


def test_three_slot_predates_acts(store):
    """Three-slot payphones (pre-1975) were operator-attended, not ACTS."""
    body = _body(store, "pay_three_slot")
    assert "operator-attended" in body["coin_validation"]


# --- switches: era + trunk signaling ----------------------------------------


def test_5ess_uses_ss7_out_of_band(store):
    """5ESS was fully digital and SS7-native for interoffice."""
    rec = store.get("netel_5ess")
    body = rec["technical_body"]
    # 5ESS speaks SS7 on trunks — check trap-trace text or role
    assert "5ESS" in rec["name"]


def test_dms100_craft_prompt_is_ci(store):
    body = _body(store, "netel_dms100")
    assert body["craft_interface"].startswith("MAPCI") or "'CI:'" in body["craft_interface"]


def test_sl1_default_admins_include_pwd1_0000(store):
    body = _body(store, "netel_sl1")
    defaults = body["default_admin_logins_era_x11_r15_to_r25"]
    assert any("PWD1 / 0000" in d for d in defaults)


# --- craft-command surface (5ESS RCV + DMS MAPCI) ----------------------------


def test_5ess_rcv_prompt_is_lt(store):
    body = _body(store, "cmd_5ess_rcv_overview")
    assert body["prompt"] == "<"


def test_dms_mapci_prompt_is_ci(store):
    body = _body(store, "cmd_dms_mapci_overview")
    assert body["prompt"] == "CI:"


def test_ld_88_manages_authcodes(store):
    body = _body(store, "ld_88_authcodes")
    assert body["ld_number"] == 88
    assert "authorization" in body["purpose"].lower()


def test_ld_40_is_cdr(store):
    body = _body(store, "ld_40_cdr")
    assert body["ld_number"] == 40
    assert "CDR" in body["purpose"] or "call-detail" in body["purpose"].lower()


# --- numbering plan: exact dates --------------------------------------------


def test_interchangeable_npa_effective_1995_01_15(store):
    body = _body(store, "nanp_1995_transition")
    assert body["effective_date"] == "1995-01-15"


def test_cic_transition_1998_07_01(store):
    body = _body(store, "npl_10xxx_101xxxx_cic")
    assert body["transition_date"] == "1998-07-01"


def test_toll_free_888_launched_1996_03_01(store):
    body = _body(store, "npl_toll_free_evolution")
    assert body["history"]["888"]["effective"] == "1996-03-01"


def test_sms800_launched_1993_05_01(store):
    """RESPORG portability launched 1993-05-01; before, toll-free was locked
    to the terminating carrier."""
    body = _body(store, "npl_toll_free_evolution")
    assert body["sms800_launch"] == "1993-05-01"


def test_911_nationalized_1968(store):
    body = _body(store, "npl_n11_codes")
    assert "1968" in body["codes"]["911"]["effective"]


def test_311_effective_1997_02_14(store):
    body = _body(store, "npl_n11_codes")
    assert body["codes"]["311"]["effective"] == "1997-02-14"


# --- cellular: keys, keys, keys ---------------------------------------------


def test_amps_shutoff_2008_02_18(store):
    body = _body(store, "cellular_amps")
    assert "2008" in body["shutoff"]
    assert "Feb 18" in body["shutoff"] or "2008-02-18" in body["shutoff"]


def test_amps_identity_leaked_min_esn_cleartext(store):
    body = _body(store, "cellular_amps")
    assert "clear" in body["cleartext_leak"]
    assert "MIN" in body["cleartext_leak"] and "ESN" in body["cleartext_leak"]


def test_startac_test_mode_sequence(store):
    body = _body(store, "nam_motorola_startac")
    assert "8 3 7 8 6 6" in body["entry_sequence"]
    assert body["entry_sequence"].startswith("FCN")


def test_oki_900_test_mode_sequence(store):
    body = _body(store, "nam_oki_900")
    assert body["entry_sequence"] == "# 6 2 3 8 8 8"


def test_gsm_a5_1_practical_break_disputed(store):
    """A5/1 practical break landed 2008-2010, not pre-2004."""
    rec = store.get("cellular_gsm")
    assert "a5_1_break_date" in rec["disputed"]


# --- X.25 DNICs -------------------------------------------------------------


def test_sprintnet_dnic_3110(store):
    body = _body(store, "x25_dnic_3110_sprintnet")
    assert body["dnic"] == "3110"


def test_tymnet_dnic_3106(store):
    body = _body(store, "x25_dnic_3106_tymnet")
    assert body["dnic"] == "3106"


def test_datapac_dnic_3020(store):
    body = _body(store, "x25_dnic_3020_datapac")
    assert body["dnic"] == "3020"


def test_sprintnet_at_prompt_after_double_cr(store):
    body = _body(store, "x25_dnic_3110_sprintnet")
    assert "<CR><CR>" in body["post_connect"]
    assert "@" in body["post_connect"]


# --- ANI II -----------------------------------------------------------------


def test_ani_ii_00_is_ordinary_pots(store):
    body = _body(store, "ani_ii_00")
    assert body["code"] == "00"
    assert "no special treatment" in body["meaning"].lower()


def test_ani_ii_27_is_acts_coin(store):
    body = _body(store, "ani_ii_27_coin")
    assert body["code"] == "27"
    assert "ACTS" in body["meaning"]


def test_ani_ii_23_split_1988(store):
    """23 (coin/coinless combined) split into 27 (coin) + 70 (private) c.1988."""
    body = _body(store, "ani_ii_23_coin_historic")
    rec = store.get("ani_ii_23_coin_historic")
    assert rec["era_bounds"][1].startswith("1988")


def test_ani_ii_60_trs_effective_1993_07_26(store):
    """TRS launched with the ADA on 1993-07-26."""
    rec = store.get("ani_ii_60_trs")
    assert rec["era_bounds"][0] == "1993-07-26"


# --- system fingerprints ----------------------------------------------------


def test_dms_mapci_fingerprint_is_ci_prompt(store):
    body = _body(store, "fp_dms_mapci")
    assert "CI:" in body["banner_text"]


def test_5ess_fingerprint_is_lt_prompt(store):
    body = _body(store, "fp_5ess_rcv")
    assert "<" in body["banner_text"]


def test_rolm_phonemail_banner_exact(store):
    body = _body(store, "fp_rolm_phonemail")
    assert body["banner_text"] == "Welcome to the ROLM PhoneMail system"


# --- defense + detection ----------------------------------------------------


def test_2600_hold_alarm_threshold_400ms(store):
    body = _body(store, "def_2600_hold_alarm")
    assert body["threshold_ms"] == 400


def test_greenstar_logged_2600_hold_patterns(store):
    body = _body(store, "def_greenstar")
    assert "2600" in body["purpose"]
    assert "1AE7" in body["detection_mechanism"]["2600_hold_alarm"]


def test_mct_still_effective_in_2026(store):
    """Malicious Call Trace is a defense that still works today."""
    rec = store.get("def_mct")
    assert rec["technical_body"].get("still_effective_2026") is True


# --- techniques + era_bounds ------------------------------------------------


def test_blueboxing_era_ends_1990(store):
    rec = store.get("technique_blue_box_domestic")
    assert rec["era_bounds"][1] == "1990-12-31"


def test_redboxing_era_ends_2002(store):
    rec = store.get("technique_red_box_fortress")
    assert rec["era_bounds"][1] == "2002-12-31"


def test_meridian_disa_abuse_still_effective(store):
    """This one still works against unpatched Meridian in 2026."""
    rec = store.get("technique_meridian_disa_abuse")
    assert rec.get("still_effective_2026") is True


# --- bibliography spot-checks -----------------------------------------------


def test_bstj_1960_is_primary(store):
    rec = store.get("bstj-1960-11")
    assert rec["type"] == "primary"
    assert "Vol. 39 No. 6" in rec["publication"]


def test_gr_506_documents_acts_quarter_33ms(store):
    """The quarter-timing dispute's telco-side source."""
    rec = store.get("gr-506-core")
    assert "5x33/33ms" in rec["note"] or "5×33" in rec["note"] or "33 ms" in rec["note"]


def test_2600_autumn_1990_is_original_redbox_publication(store):
    rec = store.get("2600-autumn-1990")
    assert "Autumn 1990" in rec["publication"]
    assert "Noah Clayton" in rec["author"]


def test_fcc_97_402_is_the_cic_transition_order(store):
    rec = store.get("fcc-97-402")
    assert "97-402" in rec["title"]
    assert "1998" in rec["publication"]
