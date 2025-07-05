import uuid
import re
from typing import Optional


class Config():
    """A class for application configuration constants."""
    LINK_PATTERN = re.compile(
        r"^(https?:\/\/)?(www\.)?([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,24}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
    )


def validate_link(link: str) -> bool:
    """Validates a URL format (with http/https, optional www, and valid domain structure)."""
    return bool(Config.LINK_PATTERN.match(link))


def generate_unique_link_id() -> str:
    """Generates a short, URL unique ID (8 chars)."""
    return uuid.uuid4().hex[:8]


def get_shortened_link(link: str) -> Optional[str]:
    """Generates a shortened link if the input is valid, else returns None."""
    if not validate_link(link):
        return None
    try:
        return f"short.lnk/{generate_unique_link_id()}"
    except Exception:
        return None


def main():
    print("Enter a URL to shorten (e.g., 'https://example.com'):")
    link = input().strip()
    final_link = get_shortened_link(link)
    print(final_link if final_link else "Invalid link provided or link generation failed.")


if __name__ == "__main__":
    main()
