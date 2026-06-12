# Beginner Explanatory Guide: PLATFORM-2987: Investigate incident runbook engine executing steps incorrectly

> **Task Type**: Product Task  
> **Domain/Focus**: Backend Automation, Python Programming

---

## 1. The Goal (In-Depth Beginner Explanation)

### The Core Problem
The incident runbook automation engine is designed to execute a series of predefined steps to remediate issues when incidents occur in a system. However, there are critical failures in its current implementation. Specifically, the engine sometimes skips essential steps or executes them in the wrong order. For example, in a sequence of steps like checking the health of a service, restarting it, and then verifying its health, the engine may skip the restart step entirely. This can lead to unresolved issues, as the necessary actions to restore service functionality are not performed.

Moreover, the conditions under which certain steps should run are not being respected. For instance, steps that are supposed to execute only if the previous step failed are running even when the previous step was successful. This not only wastes resources but can also lead to further complications in the incident resolution process. Additionally, the timeout feature, which is supposed to halt a step if it takes too long, is being ignored, causing some steps to run indefinitely. Lastly, if a step fails and has a rollback action defined, that rollback is not being executed, which can leave the system in an inconsistent state. Fixing these issues is crucial for ensuring that the incident response process is reliable and efficient, ultimately leading to better system uptime and user satisfaction.

### Jargon Buster (Key Terms Explained)
* **Runbook**: A runbook is a compilation of routine procedures and operations that system administrators or operators follow to manage and troubleshoot systems. For example, a runbook might include steps for restarting a server or checking the health of a service.
  
* **Rollback**: A rollback is a process that reverts a system to a previous state after a failure occurs. For instance, if a service restart fails, the rollback would restore the service to its last known good configuration to prevent further issues.

* **Timeout**: A timeout is a mechanism that limits the duration a process can run. If a process exceeds this limit, it is automatically terminated. For example, if a health check is supposed to complete in 30 seconds, a timeout would stop it if it runs longer than that.

* **Condition**: In programming, a condition is a statement that controls the flow of execution based on whether it evaluates to true or false. For example, a step in a runbook might only execute if the previous step failed, which is a conditional execution.

### Expected Outcome
After implementing the solution, the runbook engine should execute all steps in the correct order without skipping any. If a step is conditional, it should only run based on the defined conditions. The timeout feature should effectively halt any step that exceeds its time limit, and rollback actions should be executed whenever a step fails. 

**Before vs. After**:
- **Before**: Steps may be skipped, executed out of order, timeouts ignored, and rollbacks not executed.
- **After**: All steps execute in the correct order, respecting conditions, with timeouts enforced and rollbacks properly handled.

---

## 2. Related Coding Concepts & Syntax (50% Theory, 50% Practice)

### Concept 1: Exception Handling
#### 📘 Theoretical Overview (50%)
* **Why it exists**: Exception handling is a programming construct that allows developers to manage errors gracefully without crashing the entire application. When an error occurs, the program can catch the exception, allowing it to respond appropriately, such as logging the error or attempting a recovery action. Without exception handling, unhandled errors would lead to program crashes, resulting in a poor user experience.

* **Key Mechanisms**: In Python, exceptions are raised when an error occurs. The program can use `try` and `except` blocks to catch these exceptions. The `try` block contains code that might raise an exception, while the `except` block contains code that runs if an exception occurs. This mechanism allows for a controlled response to errors.

#### 💻 Syntax & Practical Examples (50%)
* **Language Syntax**:
  ```python
  try:
      # Code that may raise an exception
      result = risky_operation()
  except SomeSpecificException as e:
      # Code to handle the exception
      print(f"An error occurred: {e}")
  else:
      # Code that runs if no exception occurs
      print("Operation successful:", result)
  finally:
      # Code that runs no matter what
      print("Cleanup actions here.")
  ```

* **Real-World Application**:
  ```python
  def divide_numbers(a, b):
      try:
          return a / b
      except ZeroDivisionError as e:
          print("Cannot divide by zero:", e)
          return None
      finally:
          print("Execution completed.")

  result = divide_numbers(10, 0)  # This will print an error message and return None
  ```

---

## 3. Step-by-Step Logic & Walkthrough

1. **Step 1: Locate and Analyze the Target File**
   * Navigate to the `runbookEngine.py` file in the `p-w08-task-07` folder. This file contains the core logic for executing runbook steps.
   * Focus on the `execute` method, particularly the loop that iterates through `self.steps`. Pay attention to how conditions are checked and how steps are executed.

2. **Step 2: Input Verification & Validation**
   * Before executing steps, ensure that the input (the list of steps) is valid. Check for cases where the list might be empty or contain invalid step definitions.

3. **Step 3: Core Implementation / Modification**
   * Modify the `_should_run` method to correctly evaluate conditions. Ensure that it respects the conditions defined for each step, particularly for "on_failure" and "on_success" scenarios.
   * Implement the timeout logic by adding a check after executing each step to see if it has exceeded its defined timeout. If it has, set the step status to `TIMED_OUT`.
   * Ensure that rollback actions are executed when a step fails. This may involve calling the rollback function if it exists.

4. **Step 4: Output Verification & Testing**
   * After making changes, run the existing unit tests in `test_runbookEngine.py` to verify that all tests pass. If any tests fail, debug the issues based on the error messages and adjust the code accordingly.

---

## 4. Detailed Walkthrough of Test Cases

### Test Case 1: Standard / Success Case
* **Description**: This test checks if the runbook engine executes a series of steps correctly when all conditions are met.
* **Inputs**:
  ```json
  {
      "steps": [
          {
              "name": "check_health",
              "action": "StepExecutor.health_check",
              "condition": "always",
              "rollback": null,
              "timeout_seconds": 30
          },
          {
              "name": "restart_service",
              "action": "StepExecutor.restart_service",
              "condition": "on_failure",
              "rollback": "StepExecutor.create_rollback",
              "timeout_seconds": 30
          },
          {
              "name": "verify_health",
              "action": "StepExecutor.health_check",
              "condition": "on_success",
              "rollback": null,
              "timeout_seconds": 30
          }
      ]
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The engine receives the steps and begins execution.
  2. The first step, `check_health`, runs successfully, returning a healthy status.
  3. The second step, `restart_service`, is skipped because the previous step succeeded.
  4. The third step, `verify_health`, runs and confirms the service is healthy.
  5. The execution log records all steps with their statuses.

* **Expected Output**: 
  ```json
  [
      {"step": "check_health", "status": "success", "duration": 0.01},
      {"step": "restart_service", "status": "skipped", "duration": 0.0},
      {"step": "verify_health", "status": "success", "duration": 0.01}
  ]
  ```

### Test Case 2: Edge Case / Validation Fail
* **Description**: This test checks how the engine handles a situation where a step fails and requires a rollback.
* **Inputs**:
  ```json
  {
      "steps": [
          {
              "name": "check_health",
              "action": "StepExecutor.health_check",
              "condition": "always",
              "rollback": null,
              "timeout_seconds": 30
          },
          {
              "name": "restart_service",
              "action": "StepExecutor.restart_service",
              "condition": "on_failure",
              "rollback": "StepExecutor.create_rollback",
              "timeout_seconds": 30
          }
      ]
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The engine executes `check_health`, which fails (simulated failure).
  2. The second step, `restart_service`, runs because the previous step failed.
  3. The `restart_service` step also fails, triggering the rollback.
  4. The rollback function is executed, restoring the service to its previous state.
  5. The execution log records the failure and the rollback action.

* **Expected Output**: 
  ```json
  [
      {"step": "check_health", "status": "failed", "duration": 0.01, "error": "Health check failed"},
      {"step": "restart_service", "status": "failed", "duration": 0.02, "error": "Restart failed"},
      {"step": "rollback_restart_service", "status": "success", "duration": 0.01}
  ]
  ```