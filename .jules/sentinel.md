## 2024-06-23 - [Outdated Dependencies & SAST]
**Vulnerability:** Initial requirements.txt contained loose version bounds for libraries with known critical CVEs (e.g., aiohttp < 3.9.4 has CVE-2024-23334 path traversal). Missing automated dependency scanning.
**Learning:** Base repository templates often start with insecure or outdated minimum versions that expose the app to N-day vulnerabilities before any code is written.
**Prevention:** Establish secure minimum version bounds in requirements.txt, remove invalid python version specifiers, and configure automated dependency updates (Dependabot) from day one.
