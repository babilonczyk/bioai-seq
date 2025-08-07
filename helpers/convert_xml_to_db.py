import sqlite3
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm
from pathlib import Path


def extract_metadata(elem) -> dict:
    accessions = [acc.text for acc in elem.findall("./{*}accession")]
    if not accessions:
        return None

    acc = accessions[0]

    desc_elem = elem.find(".//{*}recommendedName/{*}fullName")
    org_elem = elem.find(".//{*}organism/{*}name[@type='scientific']")
    seq_elem = elem.find(".//{*}sequence")

    return {
        "id": acc,
        "description": desc_elem.text if desc_elem is not None else "",
        "organism": org_elem.text if org_elem is not None else "",
        "sequence": seq_elem.text.strip() if seq_elem is not None and seq_elem.text else "",
        "gene_names": [g.text for g in elem.findall(".//{*}gene/{*}name") if g.text],
        "organism_hosts": [
            [n.text for n in host.findall("./{*}name") if n.text]
            for host in elem.findall(".//{*}organismHost")
        ],
        "comments": [
            {
                "type": c.attrib.get("type", ""),
                "text": (c.findtext(".//{*}text") or "").strip(),
            }
            for c in elem.findall(".//{*}comment")
        ],
        "keywords": [k.text for k in elem.findall(".//{*}keyword") if k.text],
        "db_references": [
            {
                "type": db.attrib.get("type", ""),
                "id": db.attrib.get("id", ""),
                "properties": [
                    {
                        "type": prop.attrib.get("type"),
                        "value": prop.attrib.get("value"),
                    }
                    for prop in db.findall("./{*}property")
                ],
            }
            for db in elem.findall(".//{*}dbReference")
        ],
        "protein_existence": (
            elem.find(".//{*}proteinExistence").attrib.get("type", "")
            if elem.find(".//{*}proteinExistence") is not None else ""
        ),
        "features": [
            {
                "type": f.attrib.get("type", ""),
                "description": f.attrib.get("description", ""),
                "begin": f.find(".//{*}begin").attrib.get("position", "") if f.find(".//{*}begin") is not None else "",
                "end": f.find(".//{*}end").attrib.get("position", "") if f.find(".//{*}end") is not None else "",
            }
            for f in elem.findall(".//{*}feature")
        ]
    }


def save_to_sqlite(xml_file: Path, db_file: Path):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS proteins (id TEXT PRIMARY KEY, json TEXT)")
    conn.commit()

    with open(xml_file, "rb") as f:
        context = ET.iterparse(f, events=("start", "end"))
        _, root = next(context)

        for event, elem in tqdm(context, desc="Parsing XML"):
            if event == "end" and elem.tag.endswith("entry"):
                metadata = extract_metadata(elem)
                if not metadata:
                    continue

                try:
                    cursor.execute("INSERT OR IGNORE INTO proteins (id, json) VALUES (?, ?)", (
                        metadata["id"],
                        json.dumps(metadata),
                    ))
                except Exception as e:
                    print(f"❌ Error saving {metadata['id']}: {e}")

                root.clear()

    conn.commit()
    conn.close()
    print(f"✅ Saved protein metadata to {db_file}")


if __name__ == "__main__":
    save_to_sqlite(Path("swissprot.xml"), Path("proteins.db"))