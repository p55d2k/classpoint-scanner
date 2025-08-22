import asyncio
import os
import sys
import time
import threading

from src.args import parse_args
from src.constants import VERSION, START_CODE, END_CODE, AMOUNT_THREADS
from src.logger import create_links_file, log_link
from src.async_scanner import scan_codes_async
from src.api import fetch_code_info_sync
from src.is_valid_code import is_valid_code
from src.driver import get_driver
from src.verify_pool import verify_candidates


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    starttime = time.strftime("%y-%m-%d_%H:%M:%S")
    cfg = parse_args(sys.argv[1:]) if len(sys.argv) > 1 else None

    print("\033c", end="")
    print(f"classpoint-scanner v{VERSION}\nStarting search now...\n")

    output_path = None if not cfg else cfg.output
    create_links_file(starttime, output_path)

    # Single code check path
    if cfg and cfg.code is not None:
        code = int(cfg.code)
        if cfg.mode == "api":
            ok, email = fetch_code_info_sync(code)
        else:
            v = is_valid_code(code, get_driver())
            ok = bool(v and len(v) > 0 and v[0])
            email = v[1] if ok and len(v) > 1 else None
        if ok and email:
            log_link(code, str(email), output_path)
            print("Valid class code.")
            return 0
        print("Invalid class code.")
        return 1

    # Bulk scan path
    start = cfg.start if cfg else START_CODE
    end = cfg.end if cfg else END_CODE

    if not cfg or cfg.mode == "api":
        # Async API mode: fastest
        base_threads = cfg.threads if cfg else AMOUNT_THREADS
        concurrency = base_threads * 8
        candidates = asyncio.run(
            scan_codes_async(start, end, concurrency=concurrency, output_path=output_path)
        )
        if not candidates:
            print(f"Scan complete for range [{start}, {end}). No matches.")
            return 0

        # Optional verify step using Selenium to remove false positives
        if cfg and cfg.no_verify:
            for code, email in candidates:
                log_link(code, email, output_path)
            print(
                f"Scan complete for range [{start}, {end}). Links saved (no verification)."
            )
            return 0

        # Parallel Selenium verification with a small pool
        workers = max(1, min((cfg.threads if cfg else 2), 4))
        verified_pairs = verify_candidates(candidates, workers=workers)
        for code, email in verified_pairs:
            log_link(code, email, output_path)
        print(
            f"Scan complete for range [{start}, {end}). {len(verified_pairs)}/{len(candidates)} verified. Links saved."
        )
        return 0

    # Selenium mode: preserve old behavior (slower)
    amount_threads = cfg.threads

    def search_code(c, driver):
        is_valid_data = is_valid_code(c, driver)
        if not is_valid_data or not is_valid_data[0]:
            return
        if len(is_valid_data) > 1 and is_valid_data[1]:
            log_link(c, str(is_valid_data[1]), output_path)

    def search_codes(start_, end_, driver, thread_no):
        for code in range(start_, end_):
            search_code(code, driver)
        print(
            f"Search completed for thread {thread_no}, searching from {start_} to {end_}.\nLinks saved.\n"
        )

    code = start
    threads = []
    thread_increment = max(1, (end - start) // amount_threads)
    for i in range(amount_threads):
        driver = get_driver()
        thread = threading.Thread(
            target=search_codes, args=(code, min(code + thread_increment, end), driver, i + 1)
        )
        thread.daemon = True
        threads.append(thread)
        code += thread_increment
        if code >= end:
            break

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Scan complete. Links saved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
