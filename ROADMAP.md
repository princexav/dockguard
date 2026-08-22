# DockGuard Roadmap (20+ Hours Planned Work)

This roadmap outlines planned features, rule expansions, and integrations for `DockGuard`.

---

## 📍 Phase 1: Advanced Rule Engine & Multi-Stage Builds (6–8 Hours)
- [ ] **Multi-stage Build Linter:** Ensure intermediate build dependencies are stripped from final runtime images.
- [ ] **Alpine vs Debian Package Hygiene:** Specific rule checks for `apk add --no-cache` and `apt-get install -y --no-install-recommends`.
- [ ] **Sensitive File Copy Audit:** Warn when `COPY . .` or `ADD . .` copies `.git` or `.env` directories into image layers.

---

## 📍 Phase 2: Formats & CI/CD Integrations (6–8 Hours)
- [ ] **SARIF Report Exporter:** Output results in standard Static Analysis Results Interchange Format for GitHub Code Scanning tab.
- [ ] **Docker Compose Scanner:** Expand linter to validate `docker-compose.yml` service definitions (privileged mode, host volume mounts).
- [ ] **Pre-commit Hook:** Turnkey `.pre-commit-hooks.yaml` config to block commits with critical severity violations.

---

## 📍 Phase 3: Automated Fixes & Remediation (6–8 Hours)
- [ ] **Interactive Autofix (`--fix`):** Automatically inject non-root user creation and clean flags into flagged Dockerfiles.
- [ ] **Config File (`.dockguard.yaml`):** Support project-specific rule suppression and custom severity overrides.
- [ ] **Layer Size Estimator:** Estimate container layer disk consumption from unchained RUN commands.
