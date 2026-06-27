## 2024-06-27 - Automated Dependency Tracking Enabled
**Vulnerability:** Lack of automated dependency tracking (Dependabot) for pip dependencies. This leaves the project open to known vulnerabilities as packages age and new CVEs are published.
**Learning:** For a python project with many dependencies like AI tools and APIs, the risk of vulnerabilities grows rapidly over time. It's crucial to set up dependabot immediately. Furthermore, including python version requirements in `requirements.txt` breaks pip installation on standard setups, creating friction for security updates.
**Prevention:** Always create `.github/dependabot.yml` configured for `pip` on new Python projects, and avoid setting strict python versions in `requirements.txt`.
