from __future__ import annotations
import argparse
import json
from pathlib import Path
from forge.detector.stack import triage, write_manifest
from forge.hypotheses import generate_hypotheses, write_hypotheses_manifest
from forge.verification import verify_hypotheses, write_verification_manifest
from forge.sealing import read_and_verify, write_sealed_manifest
from forge.report import render_report
from forge.tiered_report import MODES, render_tiered_report

def main() -> int:
    import sys
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
        result = read_and_verify(args.verify_seal)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["ok"] else 1
    if args.repo is None:
        parser.error("repo is required unless --verify-seal is used")
    manifest = triage(args.repo)
    write_manifest(manifest, args.output)
    if args.hypotheses:
        hypotheses = generate_hypotheses(manifest)
        write_hypotheses_manifest(hypotheses, args.hypotheses)
        if args.verify:
            verification = verify_hypotheses(hypotheses)
            write_verification_manifest(verification, args.verify)
            if args.seal:
                sealed_path = args.verify.with_suffix(args.verify.suffix + ".sealed.json")
                write_sealed_manifest(verification, sealed_path)
                if args.report:
                    render_report(args.output, args.hypotheses, sealed_path, Path("forge-report.html"))
    print(args.output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
