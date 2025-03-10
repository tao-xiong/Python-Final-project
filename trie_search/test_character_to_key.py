import pytest
from trie_search.trie import character_to_key


def test_lowercase():
    assert character_to_key("a") == 0
    assert character_to_key("b") == 1
    assert character_to_key("z") == 25

def test_uppercase():
    assert character_to_key("A") == 0
    assert character_to_key("B") == 1
    assert character_to_key("Z") == 25

def test_nonalpha():
    assert character_to_key("1") == 26
    assert character_to_key("#") == 26

def test_underscore():
    assert character_to_key("_") == 26
