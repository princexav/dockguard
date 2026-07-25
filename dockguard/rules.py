import re
from dataclasses import dataclass
from typing import List
from .parser import parse_dockerfile

@dataclass
class Finding:
    rule_id: str
    severity: str # 'HIGH', 'MEDIUM', 'LOW'
    line_number: int
    message: str
    remediation: str

def scan_dockerfile(content: str) -> List[Finding]:
    instructions = parse_dockerfile(content)
    findings = []
    has_user_instruction = False
    has_healthcheck = False

    for lineno, inst, args in instructions:
        # Rule 1: Check unpinned FROM tag or latest
        if inst == "FROM":
            if ":" not in args or args.endswith(":latest"):
                findings.append(Finding(
                    rule_id="DG-001",
                    severity="HIGH",
                    line_number=lineno,
                    message=f"Base image '{args}' uses 'latest' or unpinned tag.",
                    remediation="Pin image to a specific version or SHA digest (e.g., node:18.17.0-alpine)."
                ))

        # Rule 2: Root user tracking
        if inst == "USER":
            if args.strip() not in ["root", "0"]:
                has_user_instruction = True

        # Rule 3: Healthcheck
        if inst == "HEALTHCHECK":
            has_healthcheck = True

        # Rule 4: Secret in ENV
        if inst == "ENV":
            sensitive_patterns = [r"password", r"secret", r"token", r"api_?key", r"private"]
            for pattern in sensitive_patterns:
                if re.search(pattern, args, re.IGNORECASE):
                    findings.append(Finding(
                        rule_id="DG-002",
                        severity="HIGH",
                        line_number=lineno,
                        message=f"Possible sensitive credential found in ENV directive: '{args}'.",
                        remediation="Do not hardcode secrets into Dockerfile layers. Use BuildKit secrets or runtime env."
                    ))
                    break

        # Rule 5: Risky ports (e.g. SSH 22)
        if inst == "EXPOSE":
            ports = [p.split("/")[0].strip() for p in args.split()]
            if "22" in ports:
                findings.append(Finding(
                    rule_id="DG-003",
                    severity="MEDIUM",
                    line_number=lineno,
                    message="Exposing SSH port 22 inside a container is an anti-pattern.",
                    remediation="Remove SSH server from container; access via container orchestrator instead."
                ))

    # Post-check: user
    if not has_user_instruction and instructions:
        findings.append(Finding(
            rule_id="DG-004",
            severity="HIGH",
            line_number=1,
            message="No non-root USER instruction found. Container will execute as root.",
            remediation="Add 'USER nonroot' or create a dedicated service user before ENTRYPOINT."
        ))

    # Post-check: healthcheck
    if not has_healthcheck and instructions:
        findings.append(Finding(
            rule_id="DG-005",
            severity="LOW",
            line_number=1,
            message="Missing HEALTHCHECK instruction.",
            remediation="Define a HEALTHCHECK to allow container orchestrators to monitor container health."
        ))

    return findings
