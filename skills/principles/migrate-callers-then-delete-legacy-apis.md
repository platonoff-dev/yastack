# Migrate Callers Then Delete Legacy APIs

When you introduce a new internal API while old callers still exist, migrate every caller and delete the old API in the same wave instead of keeping a compatibility layer.

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
<!-- markdownlint-disable-next-line MD032 -->
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative
