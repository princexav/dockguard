# DockGuard 🛡️

> A fast, zero-dependency static analysis and security linter for Dockerfiles.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 What is DockGuard?

Container misconfigurations are one of the most common causes of cloud security breaches. Developers frequently build Dockerfiles that run as `root`, expose unneeded ports, commit secrets, or pull untrusted `latest` tags.

**DockGuard** scans your Dockerfiles and flags issues before they reach production:
- **Root User Detection:** Enforces non-root user creation (`USER nonroot`).
- **Unpinned Base Images:** Flags risky `latest` tags on `FROM` directives.
- **Embedded Secrets:** Detects inline API keys, tokens, and sensitive environment variables in `ENV` instructions.
- **Missing Healthchecks:** Ensures production containers define health probes.
- **Package Manager Hygiene:** Flags missing `apt-get clean` or cache retention commands that bloat container size.

---

## 📦 Usage

```bash
git clone https://github.com/princexav/dockguard.git
cd dockguard
pip install -e .
```

Scan a Dockerfile:
```bash
python -m dockguard.cli scan Dockerfile
```

---

## 🧪 Testing

```bash
python -m unittest discover -s tests
```

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for 20+ hours of planned engineering milestones (SARIF export, docker-compose scanning, interactive `--fix` mode).

## 📄 License

MIT License - see [LICENSE](LICENSE).
