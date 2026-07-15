from __future__ import annotations
import argparse
import json
from pathlib import Path
from forge.sealing import read_and_verify
from forge.tiered_report import MODES, render_tiered_report
from forge.runtime import Runtime

def main() -> int:
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "audit":
        audit_parser = argparse.ArgumentParser(description="Run the complete FORGE governance runtime")
        audit_parser.add_argument("repo", type=Path)
        audit_parser.add_argument("-o", "--output-dir", type=Path, default=Path("forge-run"))
        audit_parser.add_argument("--max-connected", type=int, default=100)
        audit_args = audit_parser.parse_args(sys.argv[2:])
        result = Runtime(max_connected=audit_args.max_connected).audit(audit_args.repo, audit_args.output_dir)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        report_parser = argparse.ArgumentParser(description="Render an existing sealed FORGE artifact")
        report_parser.add_argument("sealed", type=Path)
        report_parser.add_argument("--mode", choices=MODES, default="standard")
        report_parser.add_argument("-o", "--output", type=Path)
        report_args = report_parser.parse_args(sys.argv[2:])
        print(render_tiered_report(report_args.sealed, report_args.mode, report_args.output))
        return 0
    parser = argparse.ArgumentParser(description="FORGE module 1: stack detector and triage")
    parser.add_argument("repo", type=Path, nargs="?", help="repository root (required except with --verify-seal)")
    parser.add_argument("-o", "--output", type=Path, default=Path("triage-manifest.json"))
    parser.add_argument("--hypotheses", type=Path, help="also write the module 2 hypotheses manifest")
    parser.add_argument("--verify", type=Path, help="also write the module 3 verification manifest")
    parser.add_argument("--seal", action="store_true", help="seal the verification manifest alongside it")
    parser.add_argument("--verify-seal", type=Path, help="verify a sealed verification manifest")
    parser.add_argument("--report", action="store_true", help="write forge-report.html from generated manifests")
    args = parser.parse_args()
    if args.verify_seal:
        result = Runtime().verify_findings(args.verify_seal)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["ok"] else 1
    if args.repo is None:
        parser.error("repo is required unless --verify-seal is used")
    result = Runtime().audit(args.repo, args.output.parent)
    print(result.artifacts["triage"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
