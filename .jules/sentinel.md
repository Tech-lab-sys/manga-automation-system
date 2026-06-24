## 2025-02-27 - [Dependabot configuration added & Requirements fix]
**Vulnerability:** Lack of automated dependency updates could lead to outdated dependencies with known vulnerabilities (Medium Priority). The `requirements.txt` file had `python>=3.8,<4.0`, which breaks pip installs and dependabot parsing.
**Learning:** `python>=3.8,<4.0` shouldn't be in a `requirements.txt` specifically because pip attempts to install it as a package named `python`, throwing an error.
**Prevention:** Make sure `requirements.txt` only includes installable pip packages, and use `.github/dependabot.yml` to track outdated pip packages.
