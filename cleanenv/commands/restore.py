import typer
from rich.console import Console

from cleanenv.services.restore import restore_backup
from cleanenv.services.backup import load_metadata

console = Console()


def restore(index: int = typer.Argument(None)):
    """Restore deleted environments"""

    try:
        metadata = load_metadata()
    except FileNotFoundError:
        metadata = {}

    backups = list(metadata.keys())

    if not backups:
        console.print("[green]No backups available.[/green]")
        return

    if index is None:

        console.print("\n[bold cyan]Available backups:[/bold cyan]\n")

        for i, key in enumerate(backups, start=1):
            data = metadata[key]

            console.print(
                f"{i}. {data['type']}  ({data['original_path']})"
            )

        console.print("\nRun: cleanenv restore <number>\n")
        return

    if index < 1 or index > len(backups):
        console.print("[red]Invalid backup index. Please provide a valid number from the list.[/red]")
        return

    backup_id = backups[index - 1]

    try:
        path = restore_backup(backup_id)
        console.print(f"[green]Restored to:[/green] {path}")
    except Exception as e:
        console.print(f"[red]Failed to restore backup:[/red] {e}")