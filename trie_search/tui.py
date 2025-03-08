from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from .crawler import build_index

class CrawlerSearchApp:
    def __init__(self):
        self.console = Console()
        self.trie = None

    def _get_user_input(self, prompt: str, input_type: type = str, default: Optional[str] = None) -> any:
        """
        Generalized method to get user input with optional type conversion and default value.
        
        Args:
            prompt (str): Prompt text to display
            input_type (type): Type to convert input to (default is str)
            default (Optional[str]): Default value if no input is provided
        
        Returns:
            Converted input value
        """
        while True:
            try:
                raw_input = Prompt.ask(prompt, default=default)
                return input_type(raw_input)
            except ValueError:
                self.console.print(f"[red]Invalid input. Please enter a valid {input_type.__name__}.[/red]")

    def build_index(self) -> None:
        """Build the index from user-specified URL and depth."""
        start_url = self._get_user_input("Enter the starting URL")
        max_depth = self._get_user_input("Enter the maximum depth", input_type=int, default="1")

        self.console.print("[yellow]Crawling the site and building the index...[/yellow]")
        self.trie = build_index(start_url, max_depth)
        self.console.print("[green]Index built successfully![/green]")

    def display_results(self, query: str, results: list) -> None:
        """
        Display search results in a formatted table.
        
        Args:
            query (str): Search query
            results (list): List of search results
        """
        if results:
            table = Table(
                title=Panel.fit(f"Wildcard Search Results for '{query}'", 
                                border_style="bold cyan"),
                show_header=True, 
                header_style="bold magenta"
            )
            table.add_column("Word", style="cyan", justify="left")
            table.add_column("URL", style="green", justify="left")

            for word, urls in results:
                for url in urls:
                    table.add_row(word, url)

            self.console.print(table)
        else:
            self.console.print(f"[red]No results found for '{query}'.[/red]")

    def run(self) -> None:
        """Main application run method."""
        # Build initial index
        self.build_index()

        # Search loop
        while True:
            query = Prompt.ask("Enter a search query (or type 'exit' to quit)").strip().lower()
            
            if query == "exit":
                self.console.print("[blue]Goodbye![/blue]")
                break

            # Perform search and display results
            results = list(self.trie.wildcard_search(query))
            self.display_results(query, results)

def main():
    """Entry point for the crawler search application."""
    app = CrawlerSearchApp()
    app.run()

if __name__ == "__main__":
    main()