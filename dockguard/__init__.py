"""DockGuard: Fast, lightweight Dockerfile static analysis and security linter."""

__version__ = "0.1.0"

from .parser import parse_dockerfile
from .rules import scan_dockerfile, Finding

__all__ = ["parse_dockerfile", "scan_dockerfile", "Finding"]
