import click

from scheduler import run_scheduler


@click.group()
@click.pass_context
def main(ctx: click.core.Context) -> None:
    """Initiate context.

    """


@main.command()
@click.pass_context
def runscheduler(ctx: click.core.Context) -> None:
    """Run scheduler.

    """
    run_scheduler()


if __name__ == '__main__':
    main()
