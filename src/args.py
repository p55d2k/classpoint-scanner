from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Optional

from src.constants import VERSION, START_CODE, END_CODE, AMOUNT_THREADS


@dataclass
class CliConfig:
    threads: int = AMOUNT_THREADS
    start: int = START_CODE
    end: int = END_CODE
    output: Optional[str] = None
    code: Optional[int] = None
    mode: str = "api"  # api | selenium
    no_verify: bool = False


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="classpoint-scanner")
    p.add_argument("-t", "--threads", type=int, default=AMOUNT_THREADS, help="Number of threads/workers (api mode uses async workers)")
    p.add_argument("--start", type=int, default=START_CODE, help="Start of class code range (inclusive)")
    p.add_argument("--end", type=int, default=END_CODE, help="End of class code range (exclusive)")
    p.add_argument("-o", "--output", default=None, help="Output file path. Default: links/links.txt")
    p.add_argument("-c", "--code", type=int, default=None, help="Check a single class code and exit")
    p.add_argument("-m", "--mode", choices=["api", "selenium"], default="api", help="Validation mode: api (fast) or selenium (slow)")
    p.add_argument("--no-verify", action="store_true", help="Skip Selenium verification of API-positive codes (api mode only)")
    p.add_argument("-v", "--version", action="version", version=f"classpoint-scanner v{VERSION}")
    return p


def parse_args(argv: list[str]) -> CliConfig:
    p = build_parser()
    ns = p.parse_args(argv)
    threads = max(1, min(int(ns.threads), 1024))
    if ns.start >= ns.end:
        p.error("--start must be < --end")
    return CliConfig(
        threads=threads,
        start=ns.start,
        end=ns.end,
        output=ns.output,
        code=ns.code,
        mode=ns.mode,
    no_verify=ns.no_verify,
    )
