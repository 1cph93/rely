import asyncclick as click
from rich.console import Console
from rich.table import Table

from rely.services.score_repo_service import score_repo


@click.command()
@click.argument("repo_url")
async def cli(repo_url: str) -> None:
    """Handle CLI options and render repo results to terminal."""

    await render(repo_url)


async def render(repo_url: str) -> None:
    """Render repo results to terminal."""

    repo_result = await score_repo(repo_url)

    console = Console()

    table = Table(title=f"Rely score for {repo_url}")

    table.add_column("Metric", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("Raw score", style="blue")
    table.add_column("Weight", style="yellow")
    table.add_column("Weighted score", justify="right", style="green")

    for metric in repo_result.metrics:
        table.add_row(
            metric.prettified_name,
            str(metric.metric_value),
            str(metric.metric_score),
            str(metric.metric_weight),
            str(metric.metric_weighted_score),
        )

    console.print(table)
    console.print(f"Overall score is {repo_result.overall_score_int}%")
