# Lab 5 — Reflection

**1. What is static code analysis?**

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and style violations.

**2. What issues did you identify?**

Pylint identified missing docstrings, inconsistent naming, a mutable default argument, unused imports, and other code-quality issues. Bandit identified disabled SSL verification, missing timeouts, unsafe shell execution, and legacy TLS settings. Flake8 identified formatting and style violations.

**3. How did you fix the issues?**

I improved function names and documentation, removed unused imports, replaced the mutable default argument with `None`, added an HTTP timeout, restored SSL certificate verification, replaced shell-based archiving with Python's `tarfile` module, and corrected formatting.

**4. What did you learn?**

Static analysis helps detect problems early and improves code quality, security, and maintainability. Using multiple tools is useful because each tool focuses on different types of issues.

