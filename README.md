# classpoint-scanner

## About �

Python scanner for active ClassPoint codes. Now optimized with a fast async API scanner (default) and an optional Selenium mode when you need full page validation.

## Requirements 📦

- Python 3.8+
- Pip packages: `requests`, `aiohttp`, `selenium`

Install them:

```
pip install -r requirements.txt
```

## Usage 🎯

Show help:

```
python3 main.py -h
```

Common examples:

- Scan full range (async API mode, default):
	`python3 main.py`

- Choose range and concurrency (async):
	`python3 main.py --start 10000 --end 20000 -t 8`
	(async concurrency ≈ threads*8)

- Output to a custom file:
	`python3 main.py -o links/results.txt`

- Check a single code quickly (API):
	`python3 main.py -c 12345`

- Run legacy Selenium validation (slower):
	`python3 main.py -m selenium -t 4 --start 12000 --end 13000`

Links are written to `links/links.txt` by default.

## Notes 🛠️

- Async mode massively improves throughput by avoiding browser automation.
- Selenium mode launches headless Chrome for each worker; ensure you have Chrome/Chromium and the appropriate driver available.

Created by [p55d2k](https://github.com/p55d2k)
