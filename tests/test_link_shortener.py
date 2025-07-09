from link_shortener import LinkShortener, Database, Config
import pytest
import sqlite3


@pytest.fixture
def in_memory_db():
    """Create and return an in-memory database connection."""
    db = Database(":memory:")
    return db


def test_valid_link_shortening(in_memory_db):
    shortener = LinkShortener("example.com", db=in_memory_db)

    assert shortener.validate_link()

    success, short_link = shortener.generate_shortened_link()
    assert success
    assert short_link.startswith(Config.DOMAIN)
    links = in_memory_db.get_links()
    assert short_link[-8:] in links[0]

    # Check if stored in DB
    ids = [row[0] for row in in_memory_db.get_links()]
    assert len(ids) == 1

    shortener_2 = LinkShortener("example.com", db=in_memory_db)
    assert shortener.validate_link()
    success_2, short_link_2 = shortener_2.generate_shortened_link()
    assert short_link_2.startswith(Config.DOMAIN)
    links = in_memory_db.get_links()
    assert short_link_2[-8:] in links[1][0]
    assert short_link != short_link_2


def test_database_failure_on_get_links(monkeypatch, in_memory_db):
    def fail_get_links():
        raise sqlite3.OperationalError("Simulated DB failure")

    monkeypatch.setattr(in_memory_db, "get_links", fail_get_links)

    shortener = LinkShortener("example.com", db=in_memory_db)
    success, result = shortener.generate_shortened_link()

    assert not success
    assert result is None


def test_database_failure_on_add_link(monkeypatch, in_memory_db):
    def fail_add_link():
        raise sqlite3.OperationalError("Simulated DB failure")

    monkeypatch.setattr(in_memory_db, "add_link", fail_add_link)

    shortener = LinkShortener("example.com", db=in_memory_db)
    success, result = shortener.generate_shortened_link()

    assert not success
    assert result is None


@pytest.mark.parametrize("link, expected", [
    ("abcdefg", False),
    ("htt://example.com", False),
    ("https://exa+mple.com", False),
    ("https://exa=mple.com", False),
    ("https://exa-mple.com", True),
    ("https://exa-mple.com/page-1", True),
    ("https://exa-mple.com/page-1/", True),
    ("https://example.com", True),
    ("https://example.com/", True),
    ("example.com", True),
    ("example.com/", True),
    ("www.example.com", True),
    ("www.example.com/", True),
    ("https://www.example.com/", True),
    ("https://www.example.com/page", True),
])
def test_validate_link(link, expected):
    assert LinkShortener(link).validate_link() is expected


def test_generate_unique_link_id_isolated(tmp_path, monkeypatch):
    existing_ids = {"12345678", "11111111", "aaaaaaaa"}
    assert len(LinkShortener("example.com").generate_unique_link_id(existing_ids)) == 8, "Should be 8 chars long"
    assert type(LinkShortener("example.com").generate_unique_link_id(existing_ids)) is str, "Should be of type string"


@pytest.mark.parametrize("link, expected", [
    ("abcdefg", False),
    ("htt://example.com", False),
    ("https://exa+mple.com", False),
    ("https://exa=mple.com", False),
    ("https://exa-mple.com", True),
    ("https://exa-mple.com/page-1", True),
    ("https://exa-mple.com/page-1/", True),
    ("https://example.com", True),
    ("https://example.com/", True),
    ("example.com", True),
    ("example.com/", True),
    ("www.example.com", True),
    ("www.example.com/", True),
    ("https://www.example.com/", True),
    ("https://www.example.com/page", True),
])
def test_generate_shortened_link(link, expected):
    shortener = LinkShortener(link)
    success, result = shortener.generate_shortened_link()
    if expected:
        assert success
        assert len(result.split("/")[-1]) == 8
    else:
        assert not success
