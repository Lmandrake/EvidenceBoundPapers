"""Locator stability across re-extraction (review finding SKILL.md:116, :104).

Part 1 applies the locator scheme as the OLD SKILL.md described it (position or
bare content hash) and shows drift. Part 2 applies the corrected scheme from
SKILL.md ("Locators are bound to a source version") and asserts it resolves to
the same passage or refuses.
"""
import hashlib

import pytest


def blocks_v1():
    return ["Intro.", "The contractor shall log all changes.", "Appendix.", "Footer."]


def blocks_v2_inserted():
    # parser improved: a block inserted before the cited one
    return ["Intro.", "Page header.", "The contractor shall log all changes.", "Appendix.", "Footer."]


def blocks_boilerplate():
    return ["Intro.", "Approved for release.", "Body A.", "Approved for release.", "Body B."]


# ---- OLD scheme: bare position / bare hash -------------------------------
def old_by_index(blocks, i):
    return blocks[i]


def old_by_hash(blocks, h):
    for b in blocks:
        if hashlib.sha256(b.encode()).hexdigest() == h:
            return b  # first match wins


def test_old_scheme_index_drifts():
    loc = 1  # cited "The contractor shall..." in v1
    assert old_by_index(blocks_v1(), loc) == "The contractor shall log all changes."
    # same locator against re-extraction resolves to a DIFFERENT passage, silently
    assert old_by_index(blocks_v2_inserted(), loc) != "The contractor shall log all changes."


def test_old_scheme_hash_ambiguous():
    h = hashlib.sha256(b"Approved for release.").hexdigest()
    # cited the second occurrence (block 3); bare hash resolves to the first, silently
    assert old_by_hash(blocks_boilerplate(), h) == "Approved for release."
    # and cannot tell which occurrence was meant


# ---- NEW scheme: (source_version, locator); refuse on mismatch/ambiguity ---
class Refused(Exception):
    pass


def source_version(blocks):
    return hashlib.sha256("\n".join(blocks).encode()).hexdigest()


def make_locator(blocks, index):
    return {"v": source_version(blocks), "i": index}


def make_hash_locator(blocks, index):
    return {"v": source_version(blocks), "h": hashlib.sha256(blocks[index].encode()).hexdigest()}


def resolve(blocks, loc):
    if loc["v"] != source_version(blocks):
        raise Refused("source version mismatch")
    if "i" in loc:
        return blocks[loc["i"]]
    hits = [b for b in blocks if hashlib.sha256(b.encode()).hexdigest() == loc["h"]]
    if len(hits) != 1:
        raise Refused("content hash ambiguous or absent (%d matches)" % len(hits))
    return hits[0]


def test_versioned_index_resolves_same_version():
    loc = make_locator(blocks_v1(), 1)
    assert resolve(blocks_v1(), loc) == "The contractor shall log all changes."


def test_versioned_index_refuses_after_insert():
    loc = make_locator(blocks_v1(), 1)
    with pytest.raises(Refused):
        resolve(blocks_v2_inserted(), loc)


def test_versioned_hash_refuses_repeated_boilerplate():
    bp = blocks_boilerplate()
    loc = make_hash_locator(bp, 3)
    with pytest.raises(Refused):
        resolve(bp, loc)


def test_versioned_hash_unique_passage_ok():
    loc = make_hash_locator(blocks_v1(), 1)
    assert resolve(blocks_v1(), loc) == "The contractor shall log all changes."


def test_skill_md_states_version_binding_and_refusal():
    text = open(__file__.replace("tests/test_review_2026_10_15.py", "SKILL.md")).read().lower()
    assert "source version" in text
    assert "refuse" in text and "ambiguous" in text
