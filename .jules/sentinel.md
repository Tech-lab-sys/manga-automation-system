## 2025-02-24 - [Remove Python requirement from requirements.txt]
**Vulnerability:** The line `python>=3.8,<4.0` in `requirements.txt` breaks pip installations and automated dependency tracking/scanning (like Dependabot and pip-audit) because Python is the interpreter, not a PyPI package.
**Learning:** Including the interpreter in `requirements.txt` is an anti-pattern that breaks tooling and dependency security audits.
**Prevention:** Remove Python version specifications from `requirements.txt`.
