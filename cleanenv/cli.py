import typer

from cleanenv.commands.scan import scan
from cleanenv.commands.clean import clean
from cleanenv.commands.restore import restore

app = typer.Typer()

app.command()(scan)
app.command()(clean)
app.command()(restore)

if __name__ == "__main__":
    app()