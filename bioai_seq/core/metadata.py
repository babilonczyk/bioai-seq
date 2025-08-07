import json
import requests
import typer

API_URL = "https://babilonczyk-swiss-prot.hf.space/gradio_api/call/predict"


def find_metadata_by_id(target_id: str) -> dict:
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json={"data": [target_id.strip().upper()]}
        )
        response.raise_for_status()

        event_id = response.json().get("event_id")
        if not event_id:
            typer.echo("❌ No event_id returned")
            return {}

        result_url = f"{API_URL}/{event_id}"
        with requests.get(result_url, stream=True) as stream:

            for line in stream.iter_lines():
                if line:
                    decoded = line.decode("utf-8")

                    if decoded.startswith("data: "):
                        data = json.loads(decoded[6:])

                        if isinstance(data, list) and len(data) > 0:
                            return json.loads(data[0])

        return {}

    except Exception as e:
        print(f"❌ Error fetching metadata for ID {target_id}: {e}")
        return {}
