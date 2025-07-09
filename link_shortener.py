import uuid
import re
import sqlite3
from typing import Dict, Tuple, List, Optional
import logging

class Database:
    def __init__(self, db_path="links.db"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path) if db_path != ":memory:" else sqlite3.connect(":memory:")
        self._initialize()

    def _initialize(self):
        cursor = self._conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS links(
        link_id VARCHAR(8) PRIMARY KEY,
        original_url TEXT NOT NULL
        )
        """)
        self._conn.commit()

    def get_connection(self):
        return self._conn

    def get_links(self) -> List[Tuple[str]]:
        cursor = self._conn.cursor()
        cursor.execute("""
        SELECT link_id FROM links
        """)
        return cursor.fetchall()

    def add_link(self, link, original):
        cursor = self._conn.cursor()
        cursor.execute("INSERT INTO links (link_id, original_url) VALUES (?, ?)", (link, original))
        self._conn.commit()


class Config:
    """A class for application configuration constants."""
    DOMAIN = "https://shortlinkdomain.com/"
    DOMAIN_PATTERN = r"([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,24}"
    LINK_PATTERN = re.compile(rf"^(https?://)?(www\.)?{DOMAIN_PATTERN}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*)$")


class LinkShortener:
    def __init__(self, link: str, db=None):
        """Set object's link and normalize it (add https:// in the front if not added when passing)"""
        self.link = link if link.startswith(("https://", "http://")) else f"https://{link}"
        self.db = db if db else Database()

    def validate_link(self) -> bool:
        """Validates a URL format (with http/https, optional www, and valid domain structure)."""
        return bool(Config.LINK_PATTERN.match(self.link))

    @staticmethod
    def generate_unique_link_id(existing_ids: set) -> str:
        """Generate a short, URL unique ID (8 chars)."""
        for _ in range(100):
            unique_link_id = uuid.uuid4().hex[:8]
            if unique_link_id not in existing_ids:
                return unique_link_id
        raise RuntimeError("Failed to generate unique ID")

    def generate_shortened_link(self) -> Optional[Tuple[bool, str]]:
        """Generates a shortened link if the input is valid, returns success (bool) and message(str)."""
        success = False
        if not self.validate_link():
            return success, None
        try:
            links = self.db.get_links()
            existing_ids = set(link[0] for link in links)

            shortened_id = self.generate_unique_link_id(existing_ids)
            self.db.add_link(shortened_id, self.link)

            link = f"{Config.DOMAIN}{shortened_id}"
            success = True

        except Exception as e:
            logging.info(f"[ERROR] {e}")
            link = None

        return success, link


def main():
    print("Enter a URL to shorten (e.g., 'https://example.com'):")
    link = input().strip().rstrip('/')
    link_shortener = LinkShortener(link)
    success, message = link_shortener.generate_shortened_link()
    print("✅" if success else "❌", message)


if __name__ == "__main__":
    main()
