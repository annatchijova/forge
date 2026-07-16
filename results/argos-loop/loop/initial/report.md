# FORGE audit report

Repository: `/tmp/forge-ref-n0364tut`
Seal: **VERIFIED**
Findings: **8** · Discarded hypotheses: **0**
Coverage: **23/70 (32.9%)**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 30 (16 connected)
- Domains: input_boundary
- Audit duration: 3.356646 seconds

## Findings

### HIGH · detectors/aristotle.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `return json.load(f)` at detectors/aristotle.py:22 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/aristotle.py:22: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### HIGH · detectors/foucault.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `return json.load(f)` at detectors/foucault.py:21 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/foucault.py:21: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### HIGH · detectors/gemini.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `data = json.loads(raw_text)` at detectors/gemini.py:158 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/gemini.py:158: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### HIGH · detectors/goffman.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `return json.load(f)` at detectors/goffman.py:24 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/goffman.py:24: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### HIGH · detectors/lakoff.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `return json.load(f)` at detectors/lakoff.py:26 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/lakoff.py:26: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### HIGH · detectors/searle.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `return json.load(f)` at detectors/searle.py:34 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/searle.py:34: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### HIGH · detectors/toulmin.py
- Agent: `bug_investigator`
- Status: `CONFIRMED BY INDUCTION`
- Description: The parser call `return json.load(f)` at detectors/toulmin.py:26 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Malformed input raised opaque ImportError. Evidence: detectors/toulmin.py:26: ImportError: attempted relative import with no known parent package
- Source commit: unavailable (source evidence retained)

### MEDIUM · scoring.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 47 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 14 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 9 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 7 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
