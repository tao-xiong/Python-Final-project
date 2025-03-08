import pytest
from trie_search.trie import Trie


def test_trie_set_and_get_simple():
    t = Trie()
    t["a"] = 1
    assert t["a"] == 1


def test_trie_set_and_get_longer():
    t = Trie()
    t["abc"] = 1
    assert t["abc"] == 1


def test_trie_keyerror_nonstring():
    t = Trie()
    with pytest.raises(KeyError):
        t[1234] = "abc"
    with pytest.raises(KeyError):
        t[1234]


def test_trie_keyerror_subkey():
    t = Trie()
    t["abc"] = 1
    # the substrings are not set
    with pytest.raises(KeyError):
        t["a"]
    with pytest.raises(KeyError):
        t["ab"]


def test_trie_can_set_to_none():
    # this test ensures that you can set a value to None and look it up
    # if this conflicts with how you are storing non-terminal values you'll
    # need to account for that :)
    t = Trie()
    t["will_be_none"] = None
    assert t["will_be_none"] is None


def test_trie_set_and_get_shared_prefix_first():
    t = Trie()
    # set prefix then a longer string, ensure both are kept
    t["ab"] = 1
    t["abc"] = 2
    assert t["ab"] == 1
    assert t["abc"] == 2


def test_trie_set_and_get_shared_prefix_reverse():
    t = Trie()
    # set longer string first, then prefix, both are kept
    t["abc"] = 2
    t["ab"] = 1
    assert t["ab"] == 1
    assert t["abc"] == 2


def test_trie_overwrite():
    t = Trie()
    t["abc"] = 1
    t["abc"] = 2
    assert t["abc"] == 2


def test_trie_get_keyerror():
    t = Trie()
    with pytest.raises(KeyError):
        t["a"]


def test_trie_len_basic():
    t = Trie()
    assert len(t) == 0
    t["abc"] = 1
    assert len(t) == 1


def test_trie_len_overwrite():
    t = Trie()
    t["abc"] = 1
    t["abc"] = 2
    assert len(t) == 1


def test_trie_len_long():
    t = Trie()
    for x in "abcdefghijklmnopqrstuvwxyz":
        t[x] = x
    assert len(t) == 26


def test_trie_len_case_insensitive():
    t = Trie()
    for x in "abcdeABCDE":
        t[x] = x
    assert len(t) == 5


def test_trie_len_special_chars():
    t = Trie()
    for x in "*%#./?_":
        t[x] = x
    assert len(t) == 1


def test_trie_iter_empty():
    t = Trie()
    assert list(iter(t)) == []


def test_trie_iter_one():
    t = Trie()
    t["abc"] = 1
    assert list(iter(t)) == [("abc", 1)]


def test_trie_iter_prefix_chain():
    t = Trie()
    t["a"] = 1
    t["ab"] = 2
    t["abc"] = 3
    assert list(iter(t)) == [("a", 1), ("ab", 2), ("abc", 3)]


def test_trie_iter_assorted():
    t = Trie()
    t["apple"] = 1
    t["banana"] = 2
    t["quail"] = 3
    t["quails"] = 4
    t["bees"] = 5
    assert list(iter(t)) == [
        ("apple", 1),
        ("banana", 2),
        ("bees", 5),
        ("quail", 3),
        ("quails", 4),
    ]


def test_trie_delete_one():
    t = Trie()
    t["a"] = 1
    t["b"] = 1
    del t["b"]
    assert "a" in t
    assert "b" not in t


def test_trie_delete_check_len():
    t = Trie()
    t["a"] = 1
    t["b"] = 1
    del t["b"]
    assert len(t) == 1


def test_trie_delete_nonexistent():
    t = Trie()
    with pytest.raises(KeyError):
        del t["b"]


def test_trie_delete_substring():
    t = Trie()
    t["ab"] = 1
    t["abc"] = 1
    del t["ab"]
    assert "abc" in t
    assert "ab" not in t


def test_trie_wildcard_none():
    t = Trie()
    t["ccc"] = 1
    t["aaa"] = 1
    t["bbb"] = 1
    assert list(iter(t.wildcard_search("z*"))) == []


def test_trie_wildcard_one():
    t = Trie()
    t["a"] = 1
    assert list(iter(t.wildcard_search("*"))) == [("a", 1)]


def test_trie_wildcard_multi_one():
    t = Trie()
    t["a"] = 1
    t["b"] = 1
    t["c"] = 1
    t["zzz"] = 1

    assert list(iter(t.wildcard_search("*"))) == [("a", 1), ("b", 1), ("c", 1)]


def test_trie_wildcard_multi():
    t = Trie()
    t["cat"] = 1
    t["car"] = 1
    t["cab"] = 1
    t["cot"] = 1

    assert list(iter(t.wildcard_search("ca*"))) == [("cab", 1), ("car", 1), ("cat", 1)]
    assert list(iter(t.wildcard_search("c*t"))) == [("cat", 1), ("cot", 1)]


def test_trie_wildcard_two_wildcards():
    t = Trie()
    t["cat"] = 1
    t["car"] = 1
    t["cab"] = 1
    t["cot"] = 1
    t["czz"] = 1

    assert list(iter(t.wildcard_search("c**"))) == [
        ("cab", 1),
        ("car", 1),
        ("cat", 1),
        ("cot", 1),
        ("czz", 1),
    ]


def test_trie_wildcard_all_wildcards():
    t = Trie()
    t["aaa"] = 1
    t["bbb"] = 1
    t["zzz"] = 1
    t["bb"] = 1
    t["ww"] = 1

    assert list(iter(t.wildcard_search("***"))) == [("aaa", 1), ("bbb", 1), ("zzz", 1)]
