"""Command-line interface for library embeddings."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from pathlib import Path
from .embeddings import LibraryEmbeddings

console = Console()


@click.group()
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx):
    """
    Library Embeddings: Discover Python library relationships.

    \b
    Examples:
        lib-emb similar pandas          # Find libraries similar to pandas
        lib-emb analogy flask asyncio --sub threading  # Async version of Flask
        lib-emb cluster torch           # Show ML ecosystem cluster
        lib-emb search "data"           # Search for data-related libraries

    Learn more: https://research.modelcitizendeveloper.com
    """
    # Load model once and store in context
    try:
        ctx.obj = LibraryEmbeddings()
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("\n[yellow]First time setup:[/yellow]")
        console.print("Download embeddings model:")
        console.print("  curl -o ~/.library-embeddings/model.bin https://...")
        raise click.Abort()


@main.command()
@click.argument("library")
@click.option("--top", "-n", default=10, help="Number of results")
@click.pass_obj
def similar(embeddings, library, top):
    """Find libraries similar to LIBRARY."""
    try:
        results = embeddings.similar(library, topn=top)

        table = Table(
            title=f"Libraries Similar to [bold cyan]{library}[/bold cyan]",
            box=box.ROUNDED
        )
        table.add_column("Rank", style="dim", width=6)
        table.add_column("Library", style="bold")
        table.add_column("Similarity", style="green")
        table.add_column("Bar", style="cyan")

        for i, (lib, score) in enumerate(results, 1):
            bar = "█" * int(score * 20)
            table.add_row(
                f"{i}.",
                lib,
                f"{score:.3f}",
                bar
            )

        console.print(table)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        _suggest_libraries(embeddings, library)


@main.command()
@click.argument("positive", nargs=-1, required=True)
@click.option("--sub", "--negative", "negative", multiple=True,
              help="Libraries to subtract")
@click.option("--top", "-n", default=5, help="Number of results")
@click.pass_obj
def analogy(embeddings, positive, negative, top):
    """
    Perform library analogy: POSITIVE - NEGATIVE.

    \b
    Examples:
        lib-emb analogy flask asyncio --sub threading
        → Finds: fastapi (async version of Flask)

        lib-emb analogy pandas --sub tabular
        → Finds: Libraries similar to pandas but not tabular-focused
    """
    try:
        positive_list = list(positive)
        negative_list = list(negative)

        results = embeddings.analogy(
            positive=positive_list,
            negative=negative_list,
            topn=top
        )

        # Format the equation
        pos_str = " + ".join(positive_list)
        neg_str = " - ".join(negative_list) if negative_list else ""
        equation = f"{pos_str} {('- ' + neg_str) if neg_str else ''}".strip()

        table = Table(
            title=f"Library Analogy: [bold]{equation}[/bold]",
            box=box.ROUNDED
        )
        table.add_column("Rank", style="dim", width=6)
        table.add_column("Result", style="bold cyan")
        table.add_column("Similarity", style="green")

        for i, (lib, score) in enumerate(results, 1):
            table.add_row(f"{i}.", lib, f"{score:.3f}")

        console.print(table)

        if results:
            best = results[0]
            console.print(
                f"\n[green]✓[/green] Best match: [bold]{best[0]}[/bold] "
                f"(similarity: {best[1]:.3f})"
            )

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")


@main.command()
@click.argument("library")
@click.option("--top", "-n", default=15, help="Cluster size")
@click.pass_obj
def cluster(embeddings, library, top):
    """Show ecosystem cluster for LIBRARY."""
    try:
        result = embeddings.cluster_analysis(library, topn=top)

        panel_content = f"""
[bold cyan]{library}[/bold cyan] Ecosystem Cluster

[dim]Cluster size:[/dim] {result['cluster_size']} libraries
[dim]Avg similarity:[/dim] {result['avg_similarity']:.3f}
"""

        console.print(Panel(panel_content.strip(), box=box.DOUBLE))

        table = Table(box=box.SIMPLE)
        table.add_column("Library", style="bold")
        table.add_column("Similarity", style="green")

        for lib, score in result['similar_libraries']:
            table.add_row(lib, f"{score:.3f}")

        console.print(table)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")


@main.command()
@click.argument("query")
@click.option("--top", "-n", default=10, help="Number of results")
@click.pass_obj
def search(embeddings, query, top):
    """Search for libraries matching QUERY string."""
    results = embeddings.search(query, topn=top)

    if not results:
        console.print(f"[yellow]No libraries found matching '{query}'[/yellow]")
        console.print("\nTry:")
        console.print("  - lib-emb search data")
        console.print("  - lib-emb search test")
        console.print("  - lib-emb search web")
        return

    table = Table(
        title=f"Search Results for '[cyan]{query}[/cyan]'",
        box=box.ROUNDED
    )
    table.add_column("Library", style="bold")
    table.add_column("Match", style="dim")

    for lib, _ in results:
        # Highlight query in library name
        highlighted = lib.replace(query.lower(), f"[yellow]{query.lower()}[/yellow]")
        match_type = "Exact" if lib.lower() == query.lower() else "Contains"
        table.add_row(lib, match_type)

    console.print(table)


@main.command()
@click.pass_obj
def info(embeddings):
    """Show model information."""
    model_info = embeddings.info()

    info_text = f"""
[bold]Library Embeddings Model Info[/bold]

[dim]Vocabulary size:[/dim] {model_info['vocabulary_size']} libraries
[dim]Dimensions:[/dim] {model_info['dimensions']}d
[dim]Source:[/dim] Survey of Software research

[bold]Sample libraries:[/bold]
{', '.join(model_info['sample_libraries'][:15])}...

[dim]Learn more:[/dim] https://research.modelcitizendeveloper.com
"""

    console.print(Panel(info_text.strip(), box=box.ROUNDED))


@main.command()
@click.argument("library")
@click.pass_obj
def explain(embeddings, library):
    """Get detailed explanation for LIBRARY."""
    try:
        similar = embeddings.similar(library, topn=5)

        explanation = f"""
[bold cyan]{library}[/bold cyan]

[bold]Most similar libraries:[/bold]
"""
        for lib, score in similar:
            explanation += f"  • {lib} ({score:.2f})\n"

        explanation += f"""
[bold]Usage:[/bold]
  lib-emb similar {library}        # Find alternatives
  lib-emb analogy {library} ...    # Use in analogies
  lib-emb cluster {library}        # Show ecosystem

[dim]Similarity based on co-occurrence in research + real codebases[/dim]
"""

        console.print(Panel(explanation.strip(), box=box.ROUNDED))

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        _suggest_libraries(embeddings, library)


def _suggest_libraries(embeddings, query):
    """Suggest libraries based on fuzzy search."""
    suggestions = embeddings.search(query, topn=5)
    if suggestions:
        console.print(f"\n[yellow]Did you mean:[/yellow]")
        for lib, _ in suggestions:
            console.print(f"  • {lib}")
    else:
        console.print(f"\n[dim]Try: lib-emb info  # to see available libraries[/dim]")


if __name__ == "__main__":
    main()
