import sys
import os
import argparse
from .rules import scan_dockerfile

def main():
    parser = argparse.ArgumentParser(prog="dockguard", description="Fast Dockerfile security linter.")
    subparsers = parser.add_subparsers(dest="command")

    scan_p = subparsers.add_parser("scan", help="Scan a Dockerfile for security issues")
    scan_p.add_argument("file", nargs="?", default="Dockerfile", help="Path to Dockerfile")

    args = parser.parse_args()

    if not args.command or args.command == "scan":
        filepath = getattr(args, "file", "Dockerfile")
        if not os.path.exists(filepath):
            print(f"Error: Dockerfile '{filepath}' not found.")
            sys.exit(1)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        findings = scan_dockerfile(content)
        print(f"\nDockGuard Security Scan: {filepath}")
        print("=" * 70)

        if not findings:
            print("✅ All checks passed! No security issues detected.")
            print("=" * 70 + "\n")
            sys.exit(0)

        high_count = sum(1 for f in findings if f.severity == "HIGH")
        med_count = sum(1 for f in findings if f.severity == "MEDIUM")
        low_count = sum(1 for f in findings if f.severity == "LOW")

        for f in findings:
            print(f"[{f.severity}] Line {f.line_number} ({f.rule_id}): {f.message}")
            print(f"       -> Fix: {f.remediation}\n")

        print("=" * 70)
        print(f"Summary: {high_count} HIGH, {med_count} MEDIUM, {low_count} LOW\n")
        if high_count > 0:
            sys.exit(1)

if __name__ == "__main__":
    main()
