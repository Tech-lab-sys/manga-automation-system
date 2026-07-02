## 2024-05-24 - Automated Dependency Management
**Vulnerability:** Outdated and unmonitored dependencies which are vulnerable to CVEs. Also found a `python>=3.8,<4.0` in `requirements.txt` preventing automated scanning.
**Learning:** `pip install` breaks on `python>=3.8,<4.0` which breaks Dependabot automated scanning.
**Prevention:** Remove invalid python requirements from `requirements.txt` and use automated security tools like Dependabot to monitor for outdated dependency CVEs.
