import json
import uuid
import re
from typing import Dict, Tuple
from filelock import FileLock


class Config:
    """A class for application configuration constants."""
    LINKS_PATH = "links.json"
    SHORT_DOMAIN = "https://shortlinkdomain.com/"
    DOMAIN_PATTERN = r"([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,24}"
    LINK_PATTERN = re.compile(rf"^(https?://)?(www\.)?{DOMAIN_PATTERN}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*)$")


class LinkShortener:
    def __init__(self, link: str):
        self.link = link if link.startswith(("https://", "http://")) else f"https://{link}"

    def validate_link(self) -> bool:
        """Validates a URL format (with http/https, optional www, and valid domain structure)."""
        return bool(Config.LINK_PATTERN.match(self.link))

    @staticmethod
    def generate_unique_link_id(existing_ids: set) -> str:
        """Generate a short, URL unique ID (8 chars)."""
        unique_link_id = uuid.uuid4().hex[:8]
        while unique_link_id in existing_ids:
            unique_link_id = uuid.uuid4().hex[:8]
        return unique_link_id

    @staticmethod
    def read_json_file(file: str) -> Dict[str, str]:
        """Read JSON file with lock."""
        try:
            lock_path = f"{file}.lock"

            lock = FileLock(lock_path)
            with lock.acquire(timeout=10):
                with open(file, "r") as f:
                    data = json.load(f)
        except FileNotFoundError:
            data = {}
        except TimeoutError:
            raise RuntimeError("Could not acquire lock.")

        return data

    @staticmethod
    def write_to_json_file(file: str, data: Dict[str, str]):
        """Write to JSON file with lock"""
        lock_path = f"{file}.lock"

        lock = FileLock(lock_path)
        try:
            with lock.acquire(timeout=10):
                with open(file, "w") as f:
                    json.dump(data, f, indent=4)
        except TimeoutError:
            raise RuntimeError("Could not acquire lock.")

    def generate_shortened_link(self) -> Tuple[bool, str]:
        """Generates a shortened link if the input is valid, returns success (bool) and message(str)."""
        success = False
        if not self.validate_link():
            return False, "The provided link is not valid."
        try:
            data = self.read_json_file(Config.LINKS_PATH)
            existing_ids = set(data.keys())

            shortened_id = self.generate_unique_link_id(existing_ids)
            data[shortened_id] = self.link
            self.write_to_json_file(Config.LINKS_PATH, data)

            message = f"Successfully generated shortened link: '{Config.SHORT_DOMAIN}{shortened_id}'"
            success = True

        except (TimeoutError, FileNotFoundError):
            message = "Shortened link couldn't be generated."

        return success, message


def main():
    print("Enter a URL to shorten (e.g., 'https://example.com'):")
    link = input().strip().rstrip('/')
    link_shortener = LinkShortener(link)
    print(link_shortener.generate_shortened_link())


if __name__ == "__main__":
    main()
