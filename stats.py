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


# Агрегированная статистика по хосту
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
        self._results: Dict[str, List[HostResult]] = {}

    def collect(self, results: List[HostResult]):
        for result in results:
            self._results.setdefault(result.host, []).append(result)

    def get_summary(self) -> List[HostStat]:
        summary = []
        for host, results in self._results.items():
            times = [r.time for r in results if r.status_code is not None]
            success = sum(1 for r in results if r.status_code is not None and r.status_code < 400)
            failed = sum(1 for r in results if r.status_code is not None and 400 <= r.status_code < 600)
            errors = sum(1 for r in results if r.status_code is None)

            min_time = min(times) if times else 0.0
            max_time = max(times) if times else 0.0
            avg_time = sum(times) / len(times) if times else 0.0

            stat = HostStat(
                host=host,
                success=success,
                failed=failed,
                errors=errors,
                min=min_time,
                max=max_time,
                avg=avg_time
            )
            summary.append(stat)

        return summary

