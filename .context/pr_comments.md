# PR Review - Incident runbook automation engine (by Raj)

## Reviewer: Vikram Patel
---

**Overall:** Good foundation but critical bugs need fixing before merge.

### `runbookEngine.py`

> **Bug #1:** Step dependency resolution runs steps before their prerequisites are marked complete
> This is the higher priority fix. Check the logic carefully and compare against the design doc.

### `stepExecutor.py`

> **Bug #2:** Rollback on failure does not undo already-completed steps and leaves system in partial state
> This is more subtle but will cause issues in production. Make sure to add a test case for this.

---

**Raj**
> Acknowledged. I have documented the issues for whoever picks this up.
