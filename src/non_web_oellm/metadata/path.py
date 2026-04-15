from pathlib import Path
import re
from urllib.parse import urlparse, unquote

INVALID_WINDOWS_CHARS = r'[<>:"/\\|?*]'

def sanitize_windows_name(name: str) -> str:
    # Replace invalid characters with "_"
    name = re.sub(INVALID_WINDOWS_CHARS, "_", name)

    # Avoid reserved names (CON, PRN, AUX, etc.)
    if name.upper() in {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }:
        name = f"_{name}"

    return name


def create_structure_from_url(url: str, base_path: str) -> Path:
    parsed = urlparse(url)

    # domain (with port if present)
    domain = parsed.netloc

    domain = sanitize_windows_name(domain)

    path = unquote(parsed.path).strip("/")

    folders = []
    if path:
        parts = path.split("/")

        if "." in parts[-1]:
            parts = parts[:-1]

        folders = [sanitize_windows_name(p) for p in parts]

    return Path(base_path) / domain / Path(*folders)