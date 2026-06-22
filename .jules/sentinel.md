## 2025-02-18 - [Security Enhancement] Enable Dependabot
**Vulnerability:** Missing automated dependency updates
**Learning:** Repositories without active scanning can accumulate outdated dependencies with known CVEs (e.g., in torch, OpenCV, or FastAPI).
**Prevention:** Configured `.github/dependabot.yml` to run weekly `pip` dependency checks to automate security patching.
