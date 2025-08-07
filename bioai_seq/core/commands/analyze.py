import typer

HF_API_BASE = "https://babilonczyk-facebook-esm1b-t33-650m-ur50s.hf.space/gradio_api/call/predict"


def is_fasta_file(input: str) -> bool:
    """Check if the input is a FASTA file."""
    return input.endswith('.fasta') or input.endswith('.fa')


def analyze(input: str):
    if is_fasta_file(input):
        analyze_fasta_file(input)
    else:
        analyze_sequence(input)


def analyze_fasta_file(input: str):
    typer.echo(f"🧬 Analyzing FASTA file: {input}")

    file = open(input, 'r')
    fasta_file_sequences = file.readlines()
    file.close()

    # sequence is all lines except the first one
    sequence = ''.join(fasta_file_sequences[1:]).replace('\n', '')

    # Print the sequence length
    typer.echo(f"🧬 Sequence: {sequence}")


def analyze_sequence(sequence: str):
    """Analyze a single sequence."""
    # typer.echo(f"🧬 Analyzing sequence: {sequence}")

    # Here you would add the logic to analyze the sequence
    # For now, we just print it
    # typer.echo(f"🧬 Sequence length: {len(sequence)}")
    # typer.echo(f"🧬 Sequence content: {sequence}")