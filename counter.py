import time


class OperationCounter:
    """
    Singleton or context manager to track steps and time for algorithms.
    """

    def __init__(self):
        self.steps = 0
        self.start_time = 0
        self.execution_time = 0

    def reset(self):
        self.steps = 0
        self.execution_time = 0

    def increment(self):
        """Call this method to count a step."""
        self.steps += 1

    def start(self):
        self.reset()
        self.start_time = time.perf_counter()

    def stop(self):
        self.execution_time = time.perf_counter() - self.start_time


# Global instance for simplicity in Sprint 1
perf_monitor = OperationCounter()
