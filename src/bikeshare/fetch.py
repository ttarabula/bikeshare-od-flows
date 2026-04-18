"""Fetch Bike Share Toronto data from the City of Toronto open data CKAN API.

Two relevant packages on open.toronto.ca:
  - "bike-share-toronto-ridership-data" — historical trip CSVs (published quarterly).
  - "bike-share-toronto" — station information (per-station metadata).

Package slugs are stable; resource IDs are not, so we always re-resolve via the
package_show endpoint before downloading.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import requests

CKAN_BASE = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
PACKAGE_SHOW = f"{CKAN_BASE}/api/3/action/package_show"

RIDERSHIP_PACKAGE = "bike-share-toronto-ridership-data"
STATION_PACKAGE = "bike-share-toronto"


@dataclass
class Resource:
    id: str
    name: str
    format: str
    url: str
    last_modified: str | None


def package_resources(package_id: str) -> list[Resource]:
    r = requests.get(PACKAGE_SHOW, params={"id": package_id}, timeout=30)
    r.raise_for_status()
    payload = r.json()["result"]
    return [
        Resource(
            id=res["id"],
            name=res.get("name", ""),
            format=(res.get("format") or "").lower(),
            url=res["url"],
            last_modified=res.get("last_modified"),
        )
        for res in payload.get("resources", [])
    ]


def download(resource: Resource, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Namespace filenames by resource id so we can tell revisions apart.
    tag = hashlib.sha1(resource.id.encode()).hexdigest()[:8]
    suffix = Path(resource.url).suffix or f".{resource.format}" or ".bin"
    safe_name = resource.name.replace("/", "_").replace(" ", "_")
    out = dest_dir / f"{safe_name}__{tag}{suffix}"
    if out.exists():
        return out
    with requests.get(resource.url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with out.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    return out


def save_manifest(package_id: str, resources: list[Resource], dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "package_id": package_id,
        "resources": [r.__dict__ for r in resources],
    }
    out = dest_dir / f"{package_id}.manifest.json"
    out.write_text(json.dumps(manifest, indent=2))
    return out
