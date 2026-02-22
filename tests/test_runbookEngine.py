"""Tests for Incident runbook automation engine."""
import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from runbookEngine import RunbookEngine
from stepExecutor import StepExecutor

class TestMain:
    def test_basic(self):
        obj = RunbookEngine()
        assert obj.process({"key": "val"}) is not None
    def test_empty(self):
        obj = RunbookEngine()
        assert obj.process(None) is None
    def test_stats(self):
        obj = RunbookEngine()
        obj.process({"x": 1})
        assert obj.get_stats()["processed"] == 1

class TestSupport:
    def test_basic(self):
        obj = StepExecutor()
        assert obj.process({"key": "val"}) is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
