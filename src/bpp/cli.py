"""Command line interface for bpp."""

import typer

from .interpreter import Interpreter

app = typer.Typer()


@app.callback()
def callback():
    """Brainfuck++"""


@app.command()
def run(source_file: typer.FileText):
    """Execute a file."""
    source = source_file.read()
    output = Interpreter().run(source)
    typer.echo(output)
