import json

from link_shortener import LinkShortener
import pytest


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
    monkeypatch.setattr("link_shortener.Config.LINKS_PATH", str(tmp_path / "links.json"))
    existing_ids = {"12345678", "11111111", "aaaaaaaa"}
    assert len(LinkShortener("example.com").generate_unique_link_id(existing_ids)) == 8, "Should be 8 chars long"
    assert type(LinkShortener("example.com").generate_unique_link_id(existing_ids)) is str, "Should be of type string"


def test_read_json_file(tmp_path):
    path = tmp_path / "test.json"
    path.write_text('{"key": "value"}')
    result = LinkShortener.read_json_file(str(path))
    assert result == {"key": "value"}


def test_write_to_json_file(tmp_path):
    path = tmp_path / "test.json"
    LinkShortener.write_to_json_file(str(path), {"key": "value"})
    assert json.loads(path.read_text()) == {"key": "value"}


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
    assert LinkShortener(link).generate_shortened_link()[0] is expected
