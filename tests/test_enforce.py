"""Tests for template/tools/enforce.py, the deterministic checker.

Each test copies the synthetic instance (example-synthetic/) to a temp dir, applies one
mutation, runs the checker there and asserts on the check it should trip. The synthetic
instance must read CLEAN unmutated; every failing case is that instance with one defect.

    python3 -m unittest discover -s tests -v      # or: python3 -m pytest -q tests
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENFORCE = os.path.join(REPO, "template", "tools", "enforce.py")
EXAMPLE = os.path.join(REPO, "example-synthetic")
CHECKS = ["E-%02d" % i for i in range(1, 22)]


def load_enforce():
    spec = importlib.util.spec_from_file_location("enforce_under_test", ENFORCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Instance:
    """A throwaway copy of the synthetic example."""

    def __init__(self):
        self.tmp = tempfile.mkdtemp(prefix="ebp-test-")
        self.root = os.path.join(self.tmp, "paper")
        shutil.copytree(EXAMPLE, self.root,
                        ignore=shutil.ignore_patterns(".enforcer-state.json", "enforcer-report.md"))

    def path(self, rel):
        return os.path.join(self.root, rel)

    def edit(self, rel, old, new, count=1):
        fp = self.path(rel)
        with open(fp, encoding="utf-8") as f:
            s = f.read()
        if old not in s:  # a mutation that changes nothing would test nothing
            raise AssertionError("mutation text not found in %s: %r" % (rel, old[:60]))
        with open(fp, "w", encoding="utf-8") as f:
            f.write(s.replace(old, new, count))

    def run(self):
        mod = load_enforce()
        mod.set_root(self.root)
        R, rendered, newly_failing, newly_passing, _ = mod.run()
        verdict = mod.verdict_of(R)[0]
        return mod, R, verdict

    def run_cli(self):
        return subprocess.run([sys.executable, ENFORCE, "--root", self.root, "--quiet"],
                              capture_output=True, text=True)

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.inst = Instance()

    def tearDown(self):
        self.inst.close()

    def assertFails(self, check, verdict=None, msg_part=None):
        _, R, v = self.inst.run()
        c = R.checks[check]
        self.assertEqual(c["status"], "fail", "%s should fail; msgs=%s" % (check, c["msgs"]))
        if verdict:
            self.assertEqual(v, verdict)
        if msg_part:
            self.assertTrue(any(msg_part in m for m in c["msgs"]),
                            "%r not in %s messages %s" % (msg_part, check, c["msgs"]))
        return R


# --------------------------------------------------------------------------- passing graph
class TestPassingGraph(Base):
    def test_synthetic_example_is_clean_on_every_check(self):
        _, R, v = self.inst.run()
        self.assertEqual(v, "CLEAN")
        for cid in CHECKS:
            self.assertEqual(R.checks[cid]["status"], "pass", "%s: %s" % (cid, R.checks[cid]["msgs"]))

    def test_cli_exit_code_and_report(self):
        r = self.inst.run_cli()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(self.inst.path("04-log/enforcer-report.md"), encoding="utf-8") as f:
            report = f.read()
        self.assertIn("verdict: CLEAN", report)
        self.assertIn("checks passed: 21/21", report)

    def test_unverifiable_span_is_a_warning_not_a_pass_silently(self):
        _, R, _ = self.inst.run()
        self.assertTrue(any(m.startswith("WARN ") and "quill2021" in m for m in R.checks["E-02"]["msgs"]))

    def test_unrendered_draft_defers_prose_checks(self):
        os.remove(self.inst.path("03-state/draft.md"))
        _, R, _ = self.inst.run()
        for cid in ("E-06", "E-11", "E-15", "E-16", "E-20", "E-21"):
            self.assertEqual(R.checks[cid]["status"], "na", cid)

    def test_root_without_claims_is_refused(self):
        r = subprocess.run([sys.executable, ENFORCE, "--root", self.inst.tmp],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no 03-state/claims.md", r.stderr)

    def test_empty_template_runs(self):
        tmp = tempfile.mkdtemp(prefix="ebp-tpl-")
        try:
            dst = os.path.join(tmp, "t")
            shutil.copytree(os.path.join(REPO, "template"), dst)
            r = subprocess.run([sys.executable, os.path.join(dst, "tools", "enforce.py"), "--quiet"],
                               capture_output=True, text=True)
            self.assertIn(r.returncode, (0, 1, 2), r.stderr)
            self.assertNotIn("Traceback", r.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- citations and quotes
class TestCitationsAndSpans(Base):
    def test_E01_citation_to_unknown_key_halts(self):
        self.inst.edit("03-state/claims.md", "- cite: varga2024", "- cite: varga2042")
        self.assertFails("E-01", "HALT", "varga2042")

    def test_E01_inline_remedy_citation_to_unknown_key(self):
        self.inst.edit("03-state/claims.md", "it extends [cite: halvorsen2017]", "it extends [cite: nobody2020]")
        self.assertFails("E-01", "HALT", "nobody2020")

    def test_E02_fabricated_quote_halts(self):
        # A fluent, plausible quotation that is not in the source.
        self.inst.edit("03-state/claims.md",
                       '"fewer than one in ten was ever recovered for post-deployment calibration"',
                       '"fewer than one in twenty was ever recovered for post-deployment calibration"')
        self.assertFails("E-02", "HALT", "SUP-0002 span not found verbatim in ibarra2022")

    def test_E02_real_quote_cited_to_the_wrong_source_halts(self):
        # The words exist in the corpus, but not in the cited source: a (text, location) pair
        # is verified, not mere existence.
        self.inst.edit("03-state/claims.md", "- cite: okafor2025", "- cite: varga2024")
        self.assertFails("E-02", "HALT", "SUP-0003 span not found verbatim in varga2024")

    def test_E02_strong_claim_on_unverifiable_source_halts(self):
        self.inst.edit("03-state/claims.md",
                       "- strength: Suggestive\n- tag: empirical\n- parent: TEN-01",
                       "- strength: Strong\n- tag: empirical\n- parent: TEN-01")
        self.assertFails("E-02", "HALT", "marked Strong on an unverifiable span")

    def test_E02_missing_text_cache_fails_closed(self):
        os.remove(self.inst.path("03-state/corpus-text/ibarra2022.txt"))
        self.assertFails("E-02", "HALT", "missing/empty")

    def test_E02_whitespace_differences_do_not_matter(self):
        self.inst.edit("03-state/corpus-text/ibarra2022.txt", "ever recovered", "ever\n   recovered")
        _, R, v = self.inst.run()
        self.assertEqual(R.checks["E-02"]["status"], "pass")

    def test_E16_draft_cites_key_outside_corpus(self):
        self.inst.edit("03-state/draft.md", "[ibarra2022].", "[ibarra2022, ghost2019].")
        self.assertFails("E-16", "BLOCKED", "ghost2019")

    def test_E06_citation_not_in_bound_claims(self):
        # varga2024 is in the corpus but in none of ASK-01-1's fields.
        self.inst.edit("03-state/draft.md", "derived from shared reference casts.\n",
                       "derived from shared reference casts [varga2024].\n")
        self.assertFails("E-06", "BLOCKED", "citation 'varga2024'")

    def test_E06_references_list_unknown_key(self):
        self.inst.edit("03-state/draft.md", "[varga2024] Varga", "[vargax2024] Varga")
        self.assertFails("E-06", "BLOCKED", "REFERENCES lists 'vargax2024'")


# --------------------------------------------------------------------------- failing claim graphs
class TestFailingGraphs(Base):
    def test_E03_comparative_without_baseline(self):
        self.inst.edit("03-state/claims.md",
                       "- text: In a 40-float pilot, shared-cast calibration gave a heat-content RMSE of 0.4 W m-2 compared with 1.1 W m-2 for the fleet-average adjustment.",
                       "- text: Shared-cast calibration outperforms.")
        self.assertFails("E-03", "BLOCKED", "comparative lacks baseline")

    def test_E04_causal_without_mechanism(self):
        self.inst.edit("03-state/claims.md",
                       "- mechanism: housing creep shifts the thermistor's reference resistance, so the reading drifts with time at depth (pressure-chamber tests).\n",
                       "")
        self.assertFails("E-04", "BLOCKED", "no mechanism")

    def test_E05_incidence_is_a_category_not_a_name(self):
        self.inst.edit("03-state/claims.md", "- incidence: Data Manager, Northreach Float Array Office |",
                       "- incidence: stakeholders |")
        self.assertFails("E-05", "BLOCKED", "is a category")

    def test_E07_gap_with_two_nearest_misses_halts(self):
        self.inst.edit("03-state/claims.md",
                       "  - NM-01-3 | halvorsen2017 | defines the fleet-average adjustment | removes the mean bias only\n", "")
        self.assertFails("E-07", "HALT", "2 complete nearest-miss")

    def test_E07_scope_without_search_date(self):
        self.inst.edit("03-state/claims.md", "searched 2026-10-01.", "searched recently.")
        self.assertFails("E-07", "HALT", "no search date")

    def test_E08_remedy_with_one_alternative(self):
        self.inst.edit("03-state/claims.md",
                       "  - ALT-01-1-b | model the drift from housing physics alone | the creep rate varies float to float\n", "")
        self.assertFails("E-08", "BLOCKED", "1 complete alternatives")

    def test_E09_ask_parent_is_not_a_remedy(self):
        self.inst.edit("03-state/claims.md", "- parent: REM-01-1\n- claim-type: proposed-recommendation\n- addressee",
                       "- parent: GAP-01\n- claim-type: proposed-recommendation\n- addressee")
        self.assertFails("E-09", "BLOCKED", "ASK parent is not a REMEDY")

    def test_E09_support_reaches_nothing(self):
        self.inst.edit("03-state/claims.md", "- parent: GAP-01/tractability", "- parent: GAP-99/tractability")
        self.assertFails("E-09", "BLOCKED", "SUP-0002 SUPPORT reaches no")

    def test_E10_definition_with_one_competing_view_halts(self):
        self.inst.edit("03-state/claims.md",
                       "  - Recovery view: a record is adequate if recovered floats validate it | [cite: ibarra2022] | too few floats are recovered to say.\n", "")
        R = self.assertFails("E-10", "HALT", "<2 competing")
        # and the Asserted DEF on the ASK path now fails E-17 too: the exemption needs E-10
        self.assertEqual(R.checks["E-17"]["status"], "fail")

    def test_E11_advocacy_token_in_ask_action_warns(self):
        self.inst.edit("03-state/claims.md", "- action: publish", "- action: the Halcyon Foundation should publish")
        _, R, v = self.inst.run()
        self.assertEqual(R.checks["E-11"]["status"], "fail")
        self.assertEqual(v, "CLEAN")  # WARN severity: flagged, not blocking

    def test_E12_enabling_now_outside_recency_window(self):
        self.inst.edit("03-state/claims.md", "piloted on 40 floats [cite: lindqvist2023]",
                       "piloted on 40 floats [cite: halvorsen2017]")
        self.assertFails("E-12", "BLOCKED", "no cite within 2021-2026")

    def test_E17_asserted_remedy_on_ask_path(self):
        self.inst.edit("03-state/claims.md", "- status: accepted\n- strength: Suggestive\n- parent: GAP-01\n- text: Calibrate",
                       "- status: accepted\n- strength: Asserted\n- parent: GAP-01\n- text: Calibrate")
        self.assertFails("E-17", "BLOCKED", "traverses Asserted REM-01-1")

    def test_E18_accepted_without_decision_halts(self):
        self.inst.edit("04-log/decisions.md", "REM-01-1, ASK-01-1, TEN-01", "REM-01-1, ASK-01-1")
        self.assertFails("E-18", "HALT", "TEN-01 accepted with no entry")

    def test_E18_a_pending_mention_is_not_an_admission(self):
        # decisions.md names SUP-0006 on a "- pending:" line; accepting it must still halt.
        self.inst.edit("03-state/claims.md", "- status: proposed\n- strength: Strong\n- tag: empirical\n- parent: TEN-01",
                       "- status: accepted\n- strength: Strong\n- tag: empirical\n- parent: TEN-01")
        self.assertFails("E-18", "HALT", "SUP-0006 accepted with no entry")

    def test_E18_id_ranges_on_accepted_lines_expand(self):
        self.inst.edit("04-log/decisions.md", "SUP-0001, SUP-0002, SUP-0003, SUP-0004, SUP-0005", "SUP-0001..0005")
        _, R, _ = self.inst.run()
        self.assertEqual(R.checks["E-18"]["status"], "pass", R.checks["E-18"]["msgs"])

    def test_E18_ignores_proposed_nodes(self):
        _, R, _ = self.inst.run()  # SUP-0006 is proposed and absent from the admissions
        self.assertEqual(R.checks["E-18"]["status"], "pass")

    def test_E19_tension_bears_on_nothing_known(self):
        self.inst.edit("03-state/claims.md", "- bears-on: REM-01-1", "- bears-on: REM-09-9")
        self.assertFails("E-19", "BLOCKED", "bears-on names no known node")

    def test_E20_rendered_claim_without_claim_type(self):
        self.inst.edit("03-state/claims.md", "- parent: REM-01-1\n- claim-type: proposed-recommendation\n",
                       "- parent: REM-01-1\n")
        self.assertFails("E-20", "BLOCKED", "ASK-01-1 rendered without a claim-type")

    def test_E21_inference_without_generalization_boundary(self):
        self.inst.edit("03-state/claims.md",
                       "- generalization-boundary: holds for the DeepProfiler-2 and Abyss-6K floats, which share the tested housing; says nothing about other designs.\n",
                       "")
        self.assertFails("E-21", "BLOCKED", "empty generalization-boundary")


# --------------------------------------------------------------------------- prose binding
class TestProseBinding(Base):
    def test_E06_unbound_paragraph(self):
        self.inst.edit("03-state/draft.md", "\n<!-- claims: DEF-01 -->", "")
        self.assertFails("E-06", "BLOCKED", "unbound paragraph")

    def test_E06_numeral_not_in_bound_claims(self):
        self.inst.edit("03-state/draft.md", "residual warming trend error of 0.12 W m-2",
                       "residual warming trend error of 0.15 W m-2")
        self.assertFails("E-06", "BLOCKED", "numeral '0.15'")

    def test_E06_numeral_is_matched_as_a_whole_token(self):
        # "17" occurs inside "2017" (GAP-01's scope) but never as a number of its own.
        self.inst.edit("03-state/draft.md", "carries a residual warming trend error",
                       "carries 17 residual warming trend errors")
        self.assertFails("E-06", "BLOCKED", "numeral '17'")

    def test_E06_comparative_in_bound_paragraph_must_come_from_a_claim(self):
        self.inst.edit("03-state/draft.md", "Calibrate every deep profile", "The best fix is to calibrate every deep profile")
        self.assertFails("E-06", "BLOCKED", "comparative 'best'")

    def test_E06_paragraph_bound_to_unknown_claim(self):
        self.inst.edit("03-state/draft.md", "<!-- claims: DEF-01 -->", "<!-- claims: DEF-09 -->")
        self.assertFails("E-06", "BLOCKED", "unknown claim 'DEF-09'")

    def test_E06_paragraph_bound_to_unadmitted_claim(self):
        self.inst.edit("03-state/draft.md", "<!-- claims: TEN-01, SUP-0005 -->", "<!-- claims: TEN-01, SUP-0005, SUP-0006 -->")
        self.assertFails("E-06", "BLOCKED", "SUP-0006, which is proposed")

    def test_E06_framing_may_not_carry_numbers_comparatives_or_names(self):
        self.inst.edit("03-state/draft.md", "are rarely brought home.",
                       "are rarely brought home, and most of the 40 Abyss-6K floats are the best.")
        R = self.assertFails("E-06", "BLOCKED")
        msgs = " ".join(R.checks["E-06"]["msgs"])
        self.assertIn("FRAMING paragraph contains numerals", msgs)
        self.assertIn("FRAMING paragraph contains comparatives", msgs)
        self.assertIn("FRAMING paragraph names proper nouns", msgs)

    def test_E06_identifier_digits_are_not_statistics(self):
        # With the tokens configured, "DeepProfiler-2" contributes no numeral. Without them
        # the same paragraph's digits must be traced to bound claims, so the config matters.
        mod = load_enforce()
        _, cfg = mod.parse_corpus(open(self.inst.path("03-state/corpus.md"), encoding="utf-8").read())
        self.assertEqual(cfg["identifier_tokens"], ["DeepProfiler-2", "Abyss-6K"])
        self.inst.edit("03-state/draft.md", "the DeepProfiler-2 and Abyss-6K floats",
                       "the DeepProfiler-7 and Abyss-6K floats")
        self.assertFails("E-06", "BLOCKED", "numeral '7'")

    def test_E11_advocacy_token_in_framing(self):
        self.inst.edit("03-state/draft.md", "are rarely brought home.",
                       "are rarely brought home by the Tidewater Basin Authority.")
        _, R, _ = self.inst.run()
        self.assertEqual(R.checks["E-11"]["status"], "fail")

    def test_E15_protected_text_silently_dropped_halts(self):
        self.inst.edit("03-state/draft.md", "each deep float should report its own calibration and how sure we are of it",
                       "deep floats should be better documented")
        self.assertFails("E-15", "HALT", "P-01 was present in prior draft")

    def test_E15_released_protected_text_may_go(self):
        self.inst.edit("03-state/draft.md", "each deep float should report its own calibration and how sure we are of it",
                       "each deep float should report its calibration")
        with open(self.inst.path("04-log/decisions.md"), "a", encoding="utf-8") as f:
            f.write("\n### P-01 released — 2026-10-04\n- reason: test\n")
        _, R, _ = self.inst.run()
        self.assertEqual(R.checks["E-15"]["status"], "pass")

    def test_E16_no_response_type(self):
        self.inst.edit("03-state/draft.md", "Response type: implementation. ", "")
        self.assertFails("E-16", "BLOCKED", "no declared response type")


# --------------------------------------------------------------------------- run-to-run checks
class TestRunToRun(Base):
    def test_E13_churn_without_issue_progress_warns(self):
        self.inst.edit("04-log/issues.md", "- status: closed", "- status: open")
        with open(self.inst.path("03-state/versions/draft-v001.md"), "w", encoding="utf-8") as f:
            f.write("# An unrelated earlier draft\n\nNothing alike.\n<!-- claims: FRAMING -->\n")
        R = self.assertFails("E-13", None, "with 0 issue transitions")
        self.assertEqual(R.checks["E-13"]["sev"], "WARN")

    def test_E14_regression_against_previous_run_halts(self):
        self.assertEqual(self.inst.run_cli().returncode, 0)  # stores pass states
        self.inst.edit("03-state/claims.md", "- cite: varga2024", "- cite: varga2042")
        r = self.inst.run_cli()
        self.assertEqual(r.returncode, 2)
        with open(self.inst.path("04-log/enforcer-report.md"), encoding="utf-8") as f:
            self.assertIn("REGRESSION E-01 pass->fail", f.read())

    def test_cli_exit_codes_halt_and_block(self):
        self.inst.edit("03-state/claims.md", "- bears-on: REM-01-1", "- bears-on: REM-09-9")
        self.assertEqual(self.inst.run_cli().returncode, 1)  # BLOCKED


if __name__ == "__main__":
    unittest.main()
