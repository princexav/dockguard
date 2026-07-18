import re
from typing import List, Tuple

def parse_dockerfile(content: str) -> List[Tuple[int, str, str]]:
    """
    Parses a Dockerfile content into a list of (line_number, instruction, arguments).
    Handles multi-line continuation with backslashes.
    """
    lines = content.splitlines()
    instructions = []
    
    current_line = ""
    start_lineno = 1
    
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if not current_line:
            start_lineno = lineno

        if stripped.endswith("\\"):
            current_line += stripped[:-1] + " "
        else:
            current_line += stripped
            parts = current_line.split(None, 1)
            inst = parts[0].upper()
            args = parts[1] if len(parts) > 1 else ""
            instructions.append((start_lineno, inst, args))
            current_line = ""

    return instructions
