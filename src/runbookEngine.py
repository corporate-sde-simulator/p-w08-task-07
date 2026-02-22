"""
Runbook Engine — executes incident remediation playbooks.

Runs a sequence of steps with conditions, rollbacks, and timeouts.

Author: Nisha Gupta (SRE team)
Last Modified: 2026-03-25
"""

import time
from typing import Any, Callable, Dict, List, Optional
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMED_OUT = "timed_out"


class RunbookStep:
    def __init__(self, name: str, action: Callable, condition: Optional[str] = None,
                 rollback: Optional[Callable] = None, timeout_seconds: int = 60):
        self.name = name
        self.action = action
        self.condition = condition  # "always", "on_failure", "on_success", None
        self.rollback = rollback
        self.timeout = timeout_seconds
        self.status = StepStatus.PENDING
        self.result: Any = None
        self.error: Optional[str] = None
        self.duration: float = 0


class RunbookEngine:
    def __init__(self):
        self.steps: List[RunbookStep] = []
        self.execution_log: List[Dict] = []
        self.current_step_index = 0

    def add_step(self, step: RunbookStep):
        self.steps.append(step)

    def execute(self) -> List[Dict]:
        """Execute all runbook steps in order."""
        previous_status = None

        for i, step in enumerate(self.steps):
            self.current_step_index = i

            # Check condition
            if not self._should_run(step, previous_status):
                step.status = StepStatus.SKIPPED
                self._log(step)
                continue

            # Execute the step
            step.status = StepStatus.RUNNING
            start = time.time()

            try:
                step.result = step.action()
                step.status = StepStatus.SUCCESS
            except Exception as e:
                step.status = StepStatus.FAILED
                step.error = str(e)

                if step.rollback is not None:
                    has_rollback = True

            step.duration = time.time() - start
            self._log(step)
            previous_status = step.status

        return self.execution_log

    def _should_run(self, step: RunbookStep, previous_status: Optional[StepStatus]) -> bool:
        """Decide if a step should run based on its condition and previous step result."""
        if step.condition is None or step.condition == 'always':
            return True

        if step.condition == 'on_success':
            return previous_status == StepStatus.SUCCESS

        if step.condition == 'on_failure':
            return previous_status == StepStatus.SUCCESS

        return True

    def _log(self, step: RunbookStep):
        self.execution_log.append({
            'step': step.name,
            'status': step.status.value,
            'duration': round(step.duration, 3),
            'error': step.error,
        })

    def get_summary(self) -> Dict:
        total = len(self.steps)
        by_status = {}
        for step in self.steps:
            by_status[step.status.value] = by_status.get(step.status.value, 0) + 1
        return {
            'total_steps': total,
            'by_status': by_status,
            'all_passed': all(s.status in (StepStatus.SUCCESS, StepStatus.SKIPPED) for s in self.steps),
        }
