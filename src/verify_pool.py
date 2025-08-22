from __future__ import annotations

import queue
import threading
from typing import Iterable, List, Tuple

from src.driver import get_driver
from src.is_valid_code import is_valid_code


def verify_candidates(
    candidates: Iterable[Tuple[int, str]],
    workers: int = 2,
) -> List[Tuple[int, str]]:
    """Verify (code,email) candidates using a small pool of Selenium drivers.

    Returns only verified pairs. Reuses one driver per worker to reduce overhead.
    """
    q: "queue.Queue[Tuple[int, str]]" = queue.Queue()
    for c in candidates:
        q.put(c)

    out: List[Tuple[int, str]] = []
    out_lock = threading.Lock()

    def worker():
        driver = get_driver()
        try:
            while True:
                try:
                    code, email = q.get_nowait()
                except queue.Empty:
                    break
                v = is_valid_code(code, driver)
                if v and v[0]:
                    with out_lock:
                        out.append((code, email))
                q.task_done()
        finally:
            try:
                driver.quit()
            except Exception:
                pass

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, workers))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return out
