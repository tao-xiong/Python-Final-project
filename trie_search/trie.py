from typing import Any, Iterable
from collections.abc import MutableMapping


def character_to_key(char: str) -> int:
    """
    Given a character return a number between [0, 26] inclusive.

    Letters a-z should be given their position in the alphabet 0-25, regardless of case:
        a/A -> 0
        z/Z -> 25

    Any other character should return 26.
    """
    # convert letters to index, letters are case insensitive
    if char.isalpha() and 'a' <= char.lower() <= 'z':
        return ord(char.lower()) - ord('a')
    else:
        return 26  


class TrieNode:
    '''
    This class represents the node data structure in the trie.
    '''
    def __init__(self):
        self.children = [None] * 27
        self.value = object()  # unique sentinel to distinguish unset nodes
        self.has_value = False  # flag to track if a value has been set


class Trie(MutableMapping):
    """
    Implementation of a trie class where each node in the tree can
    have up to 27 children based on next letter of key.
    (Using rules described in character_to_key.)

    Must implement all required MutableMapping methods,
    as well as wildcard_search.
    """

    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def __getitem__(self, key: str) -> Any:
        """
        Given a key, return the value associated with it in the trie.

        If the key has not been added to this trie, raise `KeyError(key)`.
        If the key is not a string, raise `KeyError(key)`(follow the test)
        """
        # check if the key is a string
        if not isinstance(key, str):
            raise KeyError(key)

        curr = self.root

        # iterate the characters in the key to move along the path in the trie
        for char in key:
            if curr.children[character_to_key(char)] is None:
                raise KeyError(key)
            curr = curr.children[character_to_key(char)]
        
        # the key does not have corresponding value
        if not curr.has_value:
            raise KeyError(key)
        return curr.value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Given a key and value, store the value associated with key.

        Like a dictionary, will overwrite existing data if key already exists.

        If the key is not a string, raise `KeyError(key)`
        """
        # check if the key is a string
        if not isinstance(key, str):
            raise KeyError(key)
        
        curr = self.root
        # iterate the characters in the key
        for char in key:
            i = character_to_key(char)
            # create new nodes when does not have the corresponding child node
            if curr.children[i] is None:
                curr.children[i] = TrieNode()
            curr = curr.children[i]
        
        # change size if created a new key-value pair
        if not curr.has_value:
            self.size += 1
        
        # set the value and mark as having a value
        curr.value = value
        curr.has_value = True

    def __delitem__(self, key: str) -> None:
        """
        Remove data associated with `key` from the trie.

        If the key is not a string, raise `KeyError(key)`
        """
        # Validate key and ensure it exists
        if not isinstance(key, str):
            raise KeyError(key)

        curr = self.root
        # Track nodes and indices to potentially remove
        path = []

        # First, traverse to find the node
        for char in key:
            index = character_to_key(char)
            if curr.children[index] is None:
                raise KeyError(key)
            path.append((curr, index))
            curr = curr.children[index]

        # Check if value exists
        if not curr.has_value:
            raise KeyError(key)

        # Remove the value and decrement size
        curr.has_value = False
        curr.value = object()  # reset to a new sentinel
        self.size -= 1

        # Clean up empty nodes from the bottom up
        for node, index in reversed(path):
            # Remove the node if it has no children and no value
            if all(child is None for child in curr.children) and not curr.has_value:
                node.children[index] = None
            curr = node

    def __len__(self) -> int:
        """
        Return the total number of entries currently in the trie.
        """
        return self.size

    def __iter__(self) -> Iterable[tuple[str, Any]]:
        """
        Return an iterable of (key, value) pairs for every entry in the trie in alphabetical order.
        """
        results = []
        # use dfs helper function to get all the pairs from top to bottom
        def dfs(node, key):
            '''
            args:
                node: the current node
                key: the current key
            '''
            # base case: the current key is valid
            if node.has_value:
                results.append((key, node.value)) 
            
            # iterate through all possible children in alphabetical order
            for index, child in enumerate(node.children):
                if child: 
                    if index < 26:
                        char = chr(index + ord('a'))
                    else:
                        char = '_'
                    dfs(child, key + char)
        
        # start from the root with an empty key
        dfs(self.root, "")
        return iter(results) # return an iterable
    
    def __repr__(self):
        """
        Override the repr
        """
        return f"The size of the trie is {self.size}, the entries are {list(self)})"

    def wildcard_search(self, key: str) -> Iterable[tuple[str, Any]]:
        """
        Search for keys that match a wildcard pattern where a '*' can represent any single character.

        For example:
            - c*t would match 'cat', 'cut', 'cot', etc.
            - ** would match any two-letter string.

        Returns: Iterable of (key, value) pairs meeting the given condition.
        """
        results = []
        def dfs(node, key, i, prefix, res):
            '''
            A helper function implements dfs to search for all the keys that match the wildcard pattern.
            args:
                node: the current node
                key: the key to search
                i: the current index in the key
                prefix: the prefix of the key
                res: the result list (key, value) pairs
            '''
            # base case1: invalid path
            if not node:
                return
            # base case2: reached the end of the key
            if i == len(key):
                if node.has_value:
                    res.append((prefix, node.value))
                return
            
            char = key[i]
            # if the current character is '*', explore all childs
            if char == '*':
                for index, child in enumerate(node.children):
                    if child:
                        char = chr(index + ord('a')) if index < 26 else '_'
                        dfs(child, key, i + 1, prefix + char, res)
            else:
                # continue the traversal
                index = character_to_key(char)
                dfs(node.children[index], key, i + 1, prefix + char, res)
        

        dfs(self.root, key, 0, "", results)
        # return iterable of results
        return iter(results)