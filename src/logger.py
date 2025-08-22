import os
from typing import Optional


def _ensure_dir(path: str):
    directory = os.path.dirname(path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)


def create_links_file(starttime: str, output_path: Optional[str] = None):
    """Create/overwrite the links file, writing the header timestamp.

    output_path: path to output file. Defaults to './links/links.txt'.
    """
    out = output_path or os.path.join("links", "links.txt")
    _ensure_dir(out)
    with open(out, "w") as f:
        f.write(f"Last updated: {starttime}\n\n")


def log_link(code: int | str, email: str, output_path: Optional[str] = None):
    out = output_path or os.path.join("links", "links.txt")
    _ensure_dir(out)
    with open(out, "a") as f:
        f.write(f"Email: {email}\nhttps://www.classpoint.app/?code={code}\n\n")

    print(f"Class code found: {code}")
    print("Link saved.\n")
