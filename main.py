import click

from scheduler import run_scheduler


@click.group()
@click.pass_context
def main(ctx: click.core.Context) -> None:
    """Initiate context.

    """


@main.command()
@click.option('--port', '-p', default=9090)
@click.pass_context
def runscheduler(ctx: click.core.Context, port: int) -> None:
    """Run scheduler.

    """
    run_scheduler(port)


if __name__ == '__main__':
    main()
