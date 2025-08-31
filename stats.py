from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class HostResult:
    host: str
    status_code: Optional[int]
    time: float

@dataclass
class HostStat:
    host: str
    success: int
    failed: int
    errors: int
    min: float
    max: float
    avg: float

class HttpPingStats:
    def __init__(self):
        self.stats: Dict[str, List[HostResult]] = {}

    def collect(self, results: List[HostResult]):
        for result in results:
            self.stats.setdefault(result.host, []).append(result)

    def print_summary(self):
        print("\n--- Статистика по каждому хосту ---\n")
        for host, results in self.stats.items():
            times = [r.time for r in results if r.status_code is not None]
            success = sum(1 for r in results if r.status_code is not None and r.status_code < 400)
            failed = sum(1 for r in results if r.status_code is not None and 400 <= r.status_code < 600)
            errors = sum(1 for r in results if r.status_code is None)

            min_time = min(times) if times else 0
            max_time = max(times) if times else 0
            avg_time = sum(times) / len(times) if times else 0

            print(f"Host    : {host}")
            print(f"  Success: {success}")
            print(f"  Failed : {failed}")
            print(f"  Errors : {errors}")
            print(f"  Min    : {min_time:.4f} sec")
            print(f"  Max    : {max_time:.4f} sec")
            print(f"  Avg    : {avg_time:.4f} sec\n")
