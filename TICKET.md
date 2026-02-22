# PLATFORM-2987: Investigate incident runbook engine executing steps incorrectly

**Status:** In Progress · **Priority:** Critical
**Sprint:** Sprint 30 · **Story Points:** 8
**Reporter:** Nisha Gupta (SRE Lead) · **Assignee:** You (Intern)
**Due:** End of sprint (Friday)
**Labels:** `backend`, `python`, `sre`, `automation`
**Task Type:** Code Debugging

---

## Description

The incident runbook automation engine executes remediation steps in order when an incident is detected. Steps are being skipped or executed in wrong order.

**DEBUGGING task — no hint comments. Investigate from symptoms.**

## Symptoms

- Runbook with steps [check_health → restart_service → verify_health] sometimes skips restart_service
- Conditional steps (only run if previous step failed) execute even when previous step succeeded
- Step timeout is ignored — a step that should timeout after 30s runs forever
- When a step fails and has a rollback action, the rollback doesn't execute

## Acceptance Criteria

- [ ] Root cause found and fixed
- [ ] Steps execute in declared order with conditions respected
- [ ] All unit tests pass
