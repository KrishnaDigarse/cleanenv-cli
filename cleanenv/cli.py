import typer
from cleanenv.commands.scan import scan
from cleanenv.commands.clean import clean
from cleanenv.commands.restore import restore

app = typer.Typer(
    help="CleanEnv: Safely clean node_modules and Python virtual environments."
)

app.command(help="Scan directories to find node_modules, venv, and other removable folders.")(scan)

app.command(help="Clean detected environments and move them to a backup location.")(clean)

app.command(help="Restore previously cleaned environments from backup.")(restore)


if __name__ == "__main__":
    app()