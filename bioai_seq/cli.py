import typer
from core import db
import core.commands.analyze as analyze_command
from pathlib import Path

app = typer.Typer()

DB_FOLDER = Path.home() / ".bioai_seq" / "db"
CHROMA_DIR = DB_FOLDER / "chroma"


@app.callback()
def setup():
    """Setup the bioai-seq environment."""
    typer.echo("🔧 Setting up bioai-seq environment...")
    if not db.is_db_installed():
        db.prompt_and_download()
    if db.is_db_installed() and not db.is_db_populated():
        db.populate_db()


@app.command()
def analyze(input: str):
    """Analyze a FASTA file or a sequence."""
    analyze_command.analyze(input)

 
if __name__ == "__main__":
    app()