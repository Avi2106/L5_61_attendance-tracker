# Lab 5 — Static Code Analysis Issue Log

| Issue | Type | Description | Fix Approach |
|---|---|---|---|
| Mutable default argument | Bug | Shared dictionary default in `mark_attendance()` | Use `None` and initialize inside the function |
| Missing HTTP timeout | Reliability | ERP request could wait indefinitely | Added `timeout=10` |
| Disabled SSL verification | Security | HTTPS certificate verification was disabled | Restored default certificate verification |
| Unsafe shell execution | Security | Backup used `subprocess` with `shell=True` | Replaced it with Python's `tarfile` module |
| Legacy TLS protocol | Security | Explicitly used TLS 1.0 | Used `ssl.create_default_context()` |
| Unused imports | Code quality | Unused imports reduced maintainability | Removed unused imports |
| Missing docstrings | Code quality | Functions and module lacked documentation | Added docstrings |
| Naming violations | Style | Functions used CamelCase names | Renamed functions to `snake_case` |
| Formatting violations | Style | Long lines and inconsistent spacing | Reformatted code and checked with Flake8 |
