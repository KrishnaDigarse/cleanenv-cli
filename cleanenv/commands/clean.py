import typer
from rich.console import Console

from cleanenv.core.scanner import scan_directory
from cleanenv.services.backup import backup_folder
from cleanenv.services.requirements import generate_requirements

console = Console()


def clean(path: str):
    """Clean environments safely"""

    console.print(f"\n[bold cyan]Cleaning environments in:[/bold cyan] {path}\n")

    results = scan_directory(path)

    if not results:
        console.print("[green]Nothing to clean.[/green]")
        return

    for r in results:

        if "venv" in r:
            generate_requirements(r)

        backup_id, backup_path = backup_folder(r)

        console.print(f"[yellow]Moved:[/yellow] {r}")
        console.print(f"[green]Backup Location:[/green] {backup_path}\n")