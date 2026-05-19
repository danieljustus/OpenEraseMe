"""CLI entrypoint for OpenEraseMe."""

from enum import StrEnum

import typer

app = typer.Typer(
    name="openeraseme",
    help="Automated data broker removal tool",
    no_args_is_help=True,
)


class OutputFormat(StrEnum):
    text = "text"
    json = "json"


@app.callback()
def main(
    ctx: typer.Context,
    output: OutputFormat = OutputFormat.text,
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["output"] = output


@app.command()
def version() -> None:
    from openeraseme import __version__

    typer.echo(f"OpenEraseMe v{__version__}")


@app.command()
def init_profile() -> None:
    typer.echo("init-profile: not yet implemented")


@app.command()
def show_profile() -> None:
    typer.echo("show-profile: not yet implemented")


if __name__ == "__main__":
    app()
