import typer
from rich.console import Console
from rich.table import Table

from cleanenv.core.scanner import scan_directory
from cleanenv.core.size import get_directory_size, human_readable

console = Console()


def scan(path: str):
    """Scan directory for environments"""

    console.print(f"\n[bold cyan]🔍 Scanning:[/bold cyan] {path}\n")

    results = scan_directory(path)

    if not results:
        console.print("[green]No environments found.[/green]")
        return

    table = Table(title="CleanEnv Results")

    table.add_column("Path", style="cyan")
    table.add_column("Size", style="magenta")

    total = 0

    for r in results:
        size = get_directory_size(r)
        total += size
        table.add_row(r, human_readable(size))

    console.print(table)

    console.print(f"\n[bold yellow]Total reclaimable:[/bold yellow] {human_readable(total)}")