## 2025-10-23 - [Dependabot Config & Dependency Cleaning]
**Vulnerability:** Unmanaged dependencies without automated security updates, combined with an invalid `python>=3.8,<4.0` entry in `requirements.txt` that breaks `pip install`.
**Learning:** This repository lacked automated vulnerability patching for its Python dependencies. Additionally, the invalid python constraint prevented installation entirely, meaning security updates could not be applied smoothly.
**Prevention:** Setup Dependabot for `pip` ecosystem to run weekly and enforce valid `requirements.txt` contents without generic python environment constraints that cause pip to fail.
