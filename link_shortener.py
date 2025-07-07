import json
import uuid
import re
from typing import Optional, Dict


class Config:
    """A class for application configuration constants."""
    SHORT_DOMAIN = "https://shortlinkdomain.com/"
    LINK_PATTERN = re.compile(
        r"^(https?://)?(www\.)?([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,24}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*)$"
    )


def validate_link(link: str) -> bool:
    """Validates a URL format (with http/https, optional www, and valid domain structure)."""
    return bool(Config.LINK_PATTERN.match(link))


def generate_unique_link_id() -> str:
    """Generates a short, URL unique ID (8 chars)."""
    try:
        with open("links.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    existing_ids = set(data.keys())
    unique_link_id = uuid.uuid4().hex[:8]
    while unique_link_id in existing_ids:
        unique_link_id = uuid.uuid4().hex[:8]
    return unique_link_id


def read_json_file(file: str) -> Dict[str: str]:
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    return data


def write_to_json_file(file: str, data: Dict[str: str]):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def generate_shortened_link(link: str) -> str:
    """Generates a shortened link if the input is valid, else returns None."""
    if not validate_link(link):
        return "The provided link is not valid."
    try:
        data = read_json_file("links.json")

        shortened_id = generate_unique_link_id()
        data[shortened_id] = link

        write_to_json_file("links.json", data)

        result = f"Successfully generated shortened link: '{Config.SHORT_DOMAIN}{shortened_id}'"

    except Exception:
        result = "Shortened link couldn't be generated."

    return result


def main():
    print("Enter a URL to shorten (e.g., 'https://example.com'):")
    link = input().strip().rstrip('/')
    print(generate_shortened_link(link))


if __name__ == "__main__":
    main()
