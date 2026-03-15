import typer
from rich.console import Console

from cleanenv.services.restore import restore_backup
from cleanenv.services.backup import METADATA_FILE
import json

console = Console()


def restore(index: int = typer.Argument(None)):
    """Restore deleted environments"""

    with open(METADATA_FILE) as f:
        metadata = json.load(f)

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

    backup_id = backups[index - 1]

    path = restore_backup(backup_id)

    console.print(f"[green]Restored to:[/green] {path}")