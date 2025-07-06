import json
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


def generate_shortened_link(link: str) -> Optional[str]:
    """Generates a shortened link if the input is valid, else returns None."""
    if not validate_link(link):
        return "The provided link is not valid."
    try:
        try:
            with open("links.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        shortened_id = generate_unique_link_id()
        while shortened_id in data.keys():
            shortened_id = generate_unique_link_id()
        data[shortened_id] = link

        with open("links.json", "w") as f:
            json.dump(data, f, indent=4)
        result = f"Successfully generated shortened link: 'https://shortlinkdomain.com/{shortened_id}'"

    except Exception:
        result = "Shortened link couldn't be generated."

    return result


def main():
    print("Enter a URL to shorten (e.g., 'https://example.com'):")
    link = input().strip()
    print(generate_shortened_link(link))


if __name__ == "__main__":
    main()
