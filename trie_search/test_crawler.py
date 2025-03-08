import pytest
from trie_search.crawler import crawl_site, build_index
from trie_search.utils import _seen_already


EXAMPLE_URL = "https://example.com"
PARKS_URL = "https://scrapple.fly.dev/parks"


# this fixture resets the internal check on if we've visited
# a URL since each test should start with a clean slate
@pytest.fixture
def fresh_seen():
    _seen_already.clear()


def test_crawl_example_com_depth0(fresh_seen):
    results = crawl_site(EXAMPLE_URL, 0)
    assert len(results) == 1
    assert "illustrative" in results[EXAMPLE_URL]
    assert "Example" in results[EXAMPLE_URL]


def test_crawl_example_com_depth1(fresh_seen):
    results = crawl_site(EXAMPLE_URL, 1)
    assert len(results) == 1


def test_crawl_parks_depth0(fresh_seen):
    results = crawl_site(PARKS_URL, 0)
    assert len(results) == 1
    assert "Chicago" in results[PARKS_URL]
    assert "Park" in results[PARKS_URL]


def test_build_index_example_com(fresh_seen):
    trie = build_index("https://example.com", 0)
    # check that a few words from the page exist
    assert trie["illustrative"] == {"https://example.com"}
    assert trie["example"] == {"https://example.com"}


def test_crawl_parks_depth1(fresh_seen):
    results = crawl_site(PARKS_URL, 1)
    assert len(results) == 12
    assert "Chicago" in results[PARKS_URL]
    assert "Park" in results[PARKS_URL]
    assert "Jensen" in results[PARKS_URL + "/4"]
    assert "almond" in results[PARKS_URL + "/10"]


def test_crawl_parks_depth2(fresh_seen):
    results = crawl_site(PARKS_URL, 2)
    assert len(results) == 24
    assert "Chicago" in results[PARKS_URL]
    assert "Park" in results[PARKS_URL]
    assert "Jensen" in results[PARKS_URL + "/4"]
    assert "almond" in results[PARKS_URL + "/10"]
    assert "Augusta" in results[PARKS_URL + "?page=3"]


def test_build_index_parks(fresh_seen):
    trie = build_index(PARKS_URL, 1)
    # check that words appear on multiple pages
    assert len(trie["park"]) == 12
    assert len(trie["chicago"]) == 12
    assert trie["baseball"] == {
        PARKS_URL + "/1",
        PARKS_URL + "/2",
        PARKS_URL + "/6",
        PARKS_URL + "/8",
    }
