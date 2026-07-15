from __future__ import annotations
import argparse
import json
from pathlib import Path
from forge.detector.stack import triage, write_manifest
from forge.hypotheses import generate_hypotheses, write_hypotheses_manifest
from forge.verification import verify_hypotheses, write_verification_manifest
from forge.sealing import read_and_verify, write_sealed_manifest

def main() -> int:
    parser = argparse.ArgumentParser(description="FORGE module 1: stack detector and triage")
    parser.add_argument("repo", type=Path, nargs="?", help="repository root (required except with --verify-seal)")
    parser.add_argument("-o", "--output", type=Path, default=Path("triage-manifest.json"))
    parser.add_argument("--hypotheses", type=Path, help="also write the module 2 hypotheses manifest")
    parser.add_argument("--verify", type=Path, help="also write the module 3 verification manifest")
    parser.add_argument("--seal", action="store_true", help="seal the verification manifest alongside it")
    parser.add_argument("--verify-seal", type=Path, help="verify a sealed verification manifest")
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
                write_sealed_manifest(verification, args.verify.with_suffix(args.verify.suffix + ".sealed.json"))
    print(args.output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
