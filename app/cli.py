import typer

app = typer.Typer()


@app.callback()
def main():
    """CleanEnv CLI"""
    pass

@app.command()
def hello():
    """Test command"""
    typer.echo("CleanEnv CLI working!")

def main():
    app()


if __name__ == "__main__":
    main()