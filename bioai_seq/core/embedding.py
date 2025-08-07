import typer
import requests

HF_API_BASE = "https://babilonczyk-facebook-esm1b-t33-650m-ur50s.hf.space/gradio_api/call/predict"


def get_embedding(sequence: str) -> list[float]:
    payload = {"data": [sequence]}
    try:
        typer.echo("🔍 Requesting embedding from remote model...")
        res = requests.post(HF_API_BASE, json=payload)
        res.raise_for_status()
        event_id = res.json().get("event_id")
        if not event_id:
            typer.echo("❌ Failed to get event_id")
            return

        # Poll result from stream endpoint
        stream_url = f"{HF_API_BASE}/{event_id}"
        with requests.get(stream_url, stream=True) as stream:
            for line in stream.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    typer.echo(decoded)
    except Exception as e:
        typer.echo("❌ Error:", str(e))