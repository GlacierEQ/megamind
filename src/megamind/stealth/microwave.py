import time
import concurrent.futures
from typing import List, Dict, Any, Callable

class StealthMicrowave:
    """Stealth Microwave Piston: Bounded parallel execution engine."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def execute_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a list of task specs in parallel threads."""
        start_time = time.time()
        if not tasks:
            return {
                "status": "BLOCKED",
                "error": "Mission tasks list cannot be empty",
                "execution_duration_sec": 0.0,
                "results": []
            }

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {}
            for task in tasks:
                task_id = task.get("task_id", "task_0")
                fn = task.get("fn", lambda: True)
                args = task.get("args", ())
                kwargs = task.get("kwargs", {})
                future = executor.submit(fn, *args, **kwargs)
                future_to_task[future] = task_id

            for future in concurrent.futures.as_completed(future_to_task):
                task_id = future_to_task[future]
                try:
                    res = future.result()
                    results.append({"task_id": task_id, "succeeded": True, "output": res})
                except Exception as e:
                    results.append({"task_id": task_id, "succeeded": False, "error": str(e)})

        duration = time.time() - start_time
        all_succeeded = all(r.get("succeeded", False) for r in results)
        results.sort(key=lambda x: x["task_id"])

        return {
            "status": "SUCCEEDED" if all_succeeded else "FAILED",
            "execution_duration_sec": round(duration, 4),
            "results": results
        }
