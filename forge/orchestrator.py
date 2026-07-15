"""Backward-compatible frontend for the canonical FORGE Runtime."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from forge.runtime import Runtime
from forge.detector.stack import triage
from forge.hypotheses import generate_hypotheses

def run_specialized_pipeline(repo: str | Path, output_dir: str | Path, max_connected: int = 100):
    return Runtime(max_connected=max_connected, triage_fn=triage).audit(repo, output_dir).to_dict()

def run_pipeline(repo: str | Path, output_dir: str | Path, max_connected: int = 100):
    return Runtime(max_connected=max_connected, triage_fn=triage).audit(repo, output_dir).to_dict()

def main() -> int:
    parser = argparse.ArgumentParser(description="Run the FORGE governance runtime")
    parser.add_argument("repo", type=Path); parser.add_argument("-o", "--output-dir", type=Path, default=Path("forge-run")); parser.add_argument("--max-connected", type=int, default=100)
    args=parser.parse_args(); print(json.dumps(run_specialized_pipeline(args.repo, args.output_dir, args.max_connected), indent=2, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
