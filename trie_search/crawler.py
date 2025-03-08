from typing import Set, Dict, List, Tuple
from .utils import get_links, get_text, fetch_html, ALLOWED_DOMAINS, FetchException
from .trie import Trie


class WebCrawler:
    """
    A web crawler that can crawl a site to depth and build an index of words to URLs.
    """
    def __init__(self, start_url: str, max_depth: int):
        """
        Initialize the web crawler with a starting URL and maximum crawl depth.

        Args:
            start_url (str): The initial URL to start crawling from
            max_depth (int): Maximum depth to crawl into the website
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited: Set[str] = set()
        self.results: Dict[str, List[str]] = {}

    def _is_valid_link(self, link: str, current_depth: int) -> bool:
        """
        Check if a link should be crawled based on depth and visited status.

        Args:
            link (str): URL to check
            current_depth (int): Current crawl depth

        Returns:
            bool: Whether the link should be crawled
        """
        return (
            current_depth <= self.max_depth and 
            link not in self.visited and 
            link.startswith(ALLOWED_DOMAINS)
        )

    def crawl(self) -> Dict[str, List[str]]:
        """
        Crawl the website and return a mapping of URLs to words.

        Returns:
            Dict[str, List[str]]: Mapping of URLs to words found on each page
        """
        queue: List[Tuple[str, int]] = [(self.start_url, 0)]

        while queue:
            url, depth = queue.pop(0)

            # Skip if link is invalid
            if not self._is_valid_link(url, depth):
                continue

            try:
                html = fetch_html(url)
            except Exception:
                continue

            # Process the page
            self._process_page(url, html, depth, queue)

        return self.results

    def _process_page(self, url: str, html: str, depth: int, queue: List[Tuple[str, int]]):
        """
        Process a single page during crawling.

        Args:
            url (str): URL of the current page
            html (str): HTML content of the page
            depth (int): Current crawl depth
            queue (List[Tuple[str, int]]): Queue of URLs to crawl
        """
        self.visited.add(url)
        words = get_text(html).split()
        self.results[url] = words

        if depth < self.max_depth:
            links = get_links(html, url)
            new_links = [
                (link, depth + 1) 
                for link in links 
                if self._is_valid_link(link, depth + 1)
            ]
            queue.extend(new_links)

    def build_index(self) -> Trie:
        """
        Build a Trie index of words to URLs.

        Returns:
            Trie: Indexed words mapped to URLs
        """
        # If crawl hasn't been performed, perform it
        if not self.results:
            self.crawl()

        trie = Trie()
        for url, words in self.results.items():
            for word in words:
                # Normalize word to lowercase
                word = word.lower()
                if word not in trie:
                    trie[word] = set()
                trie[word].add(url)

        return trie


# Convenience functions maintaining original interface
def crawl_site(start_url: str, max_depth: int) -> Dict[str, List[str]]:
    """
    Compatibility wrapper for the original crawl_site function.
    
    Args:
        start_url (str): URL to start crawling
        max_depth (int): Maximum crawl depth
    
    Returns:
        Dict[str, List[str]]: Mapping of URLs to words
    """
    crawler = WebCrawler(start_url, max_depth)
    return crawler.crawl()


def build_index(site_url: str, max_depth: int) -> Trie:
    """
    Compatibility wrapper for the original build_index function.
    
    Args:
        site_url (str): URL to start crawling
        max_depth (int): Maximum crawl depth
    
    Returns:
        Trie: Indexed words mapped to URLs
    """
    crawler = WebCrawler(site_url, max_depth)
    return crawler.build_index()