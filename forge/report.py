"""Self-contained, evidence-first HTML report renderer for module 5."""
from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path
from typing import Any

from forge.sealing import verify_sealed


def _e(value: Any) -> str:
    return html.escape(str(value))


def _load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _blame(root: str, module_path: str, line: int) -> str | None:
    try:
        raw = subprocess.check_output(
            ["git", "-C", root, "blame", "--line-porcelain", "-L", f"{line},{line}", "--", module_path],
            stderr=subprocess.DEVNULL, text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    fields = {}
    for row in raw.splitlines():
        key, _, value = row.partition(" ")
        if key in {"author", "author-time", "summary"}:
            fields[key] = value
        elif not fields.get("commit") and len(row.split()) >= 3 and not row.startswith(("author ", "author-time ")):
            fields["commit"] = row.split()[0]
    if not fields:
        return None
    return f"author={fields.get('author', 'unknown')}; date={fields.get('author-time', 'unknown')}; commit={fields.get('commit', 'unknown')}"


def _hypothesis_for(hypotheses: list[dict[str, Any]], module: str, line: int) -> dict[str, Any] | None:
    return next((h for h in hypotheses if h.get("module_path") == module and line in h.get("file_lines", [])), None)


def _finding_card(finding: dict[str, Any], hypotheses: list[dict[str, Any]], root: str) -> str:
    evidence = finding.get("evidence", [])
    source = next((item for item in evidence if item.get("kind") == "source"), evidence[0] if evidence else {})
    source_ref = source.get("source", "unknown")
    module, _, line_text = source_ref.rpartition(":")
    try:
        line = int(line_text)
    except ValueError:
        line = 0
    hypothesis = _hypothesis_for(hypotheses, finding.get("module_path", module), line)
    blame = _blame(root, module or finding.get("module_path", ""), line) if line else None
    blame_html = _e(blame) if blame else "Git blame unavailable for this line; report continues with source evidence only."
    falsifier = hypothesis.get("falsification_test", "No originating hypothesis test was found in the supplied manifest.") if hypothesis else "No originating hypothesis test was found in the supplied manifest."
    return f"""<article class=\"finding\">
      <div><span class=\"badge\">{_e(finding.get('epistemic_level', ''))}</span> <span class=\"ref\">{_e(source_ref)}</span></div>
      <p><strong>Description (inference):</strong> {_e(finding.get('description', ''))}</p>
      <p><strong>Source observation:</strong> <code>{_e(source.get('detail', ''))}</code></p>
      <p><strong>Reasoning:</strong> {_e(finding.get('reasoning', ''))}</p>
      <p><strong>Falsification test:</strong> {_e(falsifier)}</p>
      <p><strong>Additional evidence — git blame:</strong> {_e(blame_html)}</p>
    </article>"""


def render_report(triage_path: str | Path, hypotheses_path: str | Path, sealed_path: str | Path, destination: str | Path) -> None:
    triage = _load(triage_path)
    hypotheses_doc = _load(hypotheses_path)
    sealed = _load(sealed_path)
    seal = verify_sealed(sealed)
    manifest = sealed.get("manifest", {})
    findings = [entry.get("finding", {}) for entry in sealed.get("chain", [])]
    hypotheses = hypotheses_doc.get("hypotheses", [])
    root = triage.get("root", manifest.get("root", "."))
    finding_modules = {f.get("module_path") for f in findings}
    discarded = manifest.get("discarded", [])
    audited = hypotheses_doc.get("audited_modules", [])
    clean = [module for module in audited if module not in finding_modules]
    out_of_scope = [m for m in triage.get("modules", []) if m.get("module_class") != "CONNECTED_ALIVE"]
    families = ", ".join(manifest.get("ast_verified_families", [])) or "the implemented structural checks"
    seal_text = f"Chain integrity: VERIFIED ({len(sealed.get('chain', []))} entries, 0 issues)" if seal["ok"] else f"Chain integrity: FAILED ({len(sealed.get('chain', []))} entries, {len(seal['issues'])} issues): {'; '.join(seal['issues'])}"
    git_note = "Git blame is attempted per finding and is shown when available; unavailable blame is labeled rather than inferred."
    findings_html = "".join(_finding_card(f, hypotheses, root) for f in findings) or "<p>No surviving findings in the supplied sealed manifest.</p>"
    discarded_html = "".join(f"<article class=\"discarded\"><strong>{_e(item.get('module_path'))}</strong><p>{_e(item.get('reason'))}</p></article>" for item in discarded) or "<p>No discarded hypotheses recorded.</p>"
    clean_html = "".join(f"<li>{_e(module)} — checked against: {_e(families)}</li>" for module in clean) or "<li>No audited module met the clean-module condition.</li>"
    scope_html = "".join(f"<article class=\"scope\"><strong>{_e(item.get('path'))}</strong> — {_e(item.get('module_class'))}. This module was outside CONNECTED_ALIVE scope for this run.</article>" for item in out_of_scope) or "<p>All triaged modules were in CONNECTED_ALIVE scope.</p>"
    limitations = "The seal shows that sealed findings were not altered after sealing; it does not show that findings are correct. It does not protect against a full cascade forgery or truncation with an edited reported_chain_length. <a href=\"DECISIONS.md\">DECISIONS.md</a> records the bounds."
    document = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>FORGE report</title>
<style>body{{font:16px system-ui,sans-serif;line-height:1.45;color:#202124;max-width:1100px;margin:2rem auto;padding:0 1rem}}header{{border:3px solid #333;padding:1rem;margin-bottom:2rem}}h1{{margin-top:0}}section{{border:1px solid #aaa;margin:1.5rem 0;padding:1rem}}section h2{{margin-top:0;padding-bottom:.5rem;border-bottom:3px solid}}#findings h2{{color:#174a7e}}#discarded h2{{color:#725400}}#scope h2{{color:#6b3030}}.finding,.discarded,.scope{{border:1px solid #ddd;padding:1rem;margin:1rem 0}}.badge{{background:#eee;border:1px solid #555;padding:.2rem .5rem;font-weight:700}}.ref{{font-family:monospace}}code{{display:block;white-space:pre-wrap;background:#f4f4f4;padding:.6rem}}.ok{{color:#086b36}}.fail{{color:#9b1c1c}}small{{color:#555}}</style></head><body>
<header><h1>FORGE verification report</h1><h2 class=\"{'ok' if seal['ok'] else 'fail'}\">{_e(seal_text)}</h2><p>{limitations}</p><p><small>{_e(git_note)}</small></p></header>
<section id=\"findings\"><h2>FINDINGS</h2>{findings_html}</section>
<section id=\"discarded\"><h2>DISCARDED</h2><p>Generated hypotheses ruled out by the verification criteria are retained here with their reasons.</p>{discarded_html}</section>
<section id=\"clean\"><h2>No structural risk indicators found</h2><p>Audited modules with zero surviving findings:</p><ul>{clean_html}</ul></section>
<section id=\"scope\"><h2>NOT ANALYZED</h2><p>These triaged modules were not analyzed in this run because they were not classified as CONNECTED_ALIVE:</p>{scope_html}</section>
</body></html>"""
    Path(destination).write_text(document, encoding="utf-8")
