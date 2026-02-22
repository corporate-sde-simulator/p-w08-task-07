"""
Step Executor — helper utilities for common runbook step types.

Provides pre-built step actions for health checks, restarts, etc.

Author: Nisha Gupta (SRE team)
Last Modified: 2026-03-25
"""

import time
import random
from typing import Dict, Optional


class StepExecutor:
    """Pre-built step actions for common incident remediation tasks."""

    @staticmethod
    def health_check(service_name: str, endpoint: str = '/health') -> Dict:
        """Check if a service is healthy."""
        # Simulated health check
        time.sleep(0.01)
        healthy = random.random() > 0.1  # 90% chance healthy
        return {
            'service': service_name,
            'endpoint': endpoint,
            'healthy': healthy,
            'response_time_ms': random.randint(5, 100),
        }

    @staticmethod
    def restart_service(service_name: str) -> Dict:
        """Restart a service."""
        time.sleep(0.05)
        return {
            'service': service_name,
            'action': 'restart',
            'success': True,
            'downtime_ms': random.randint(500, 2000),
        }

    @staticmethod
    def scale_service(service_name: str, replicas: int) -> Dict:
        """Scale a service to N replicas."""
        time.sleep(0.02)
        return {
            'service': service_name,
            'action': 'scale',
            'target_replicas': replicas,
            'current_replicas': replicas,
            'success': True,
        }

    @staticmethod
    def clear_cache(cache_name: str) -> Dict:
        """Clear a named cache."""
        time.sleep(0.01)
        return {
            'cache': cache_name,
            'action': 'clear',
            'entries_cleared': random.randint(100, 10000),
            'success': True,
        }

    @staticmethod
    def create_rollback(service_name: str, action: str):
        """Create a rollback function for a given action."""
        def rollback():
            time.sleep(0.02)
            return {
                'service': service_name,
                'action': f'rollback_{action}',
                'success': True,
            }
        return rollback
