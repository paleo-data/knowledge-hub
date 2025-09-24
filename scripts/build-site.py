"""Creates and indexes pages based using YAML files in _data"""

import re
import shutil
from datetime import date
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

try:
    import requests_cache
except ModuleNotFoundError:
    import requests

from const import BASEPATH
from utils import (
    add_tooltips,
    autolink,
    build_nav,
    compute_urls,
    index_tags,
    read_fms,
    to_slug,
)

if __name__ == "__main__":

    # Use cache when building the site locally. Cached requests expire after 8 hrs.
    try:
        session = requests_cache.CachedSession(expire_after=28800)
    except NameError:
        session = requests.Session()

    # Update resources from Zenodo
    res_path = Path(BASEPATH / "_data" / "resources")
    upd_path = Path(BASEPATH / "_data" / "resources-updated")
    for path in [res_path, upd_path]:
        path.mkdir(parents=True, exist_ok=True)

    print("Updating resources")
    for path_ in res_path.glob("*.yml"):

        with open(path_, encoding="utf-8") as f:
            rec = yaml.safe_load(f.read())

        # Fill in Zenodo records
        doi = rec.get("doi")
        match = re.search(r"https?://doi.org/10.5281/zenodo.(\d+)$", doi if doi else "")
        if match:
            resp = session.get(f"https://zenodo.org/api/records/{match.group(1)}")
            zrec = resp.json()
            metadata = zrec["metadata"]
            desc = BeautifulSoup(metadata["description"], "html5lib")

            names = [p["name"] for p in metadata["creators"]]
            year = metadata["publication_date"][:4]
            last_names = [n.split(",")[0] for n in names]
            if len(last_names) == 1:
                citation = f"{last_names[0]} ({year})"
            elif len(last_names) == 2:
                citation = f"{last_names[0]} and {last_names[1]} ({year})"
            else:
                citation = f"{last_names[0]} et al. ({year})"

            # The value in path is used in a link tag, which expects the location of
            # the file in the _site directory. Note that those paths omit the
            # collections directory (defined in collections_dir in the config file).
            row = {
                "citation": citation,
                "title": metadata["title"],
                "creators": "; ".join(names),
                "description": autolink(re.sub("\n{2,}", "\n\n", desc.text)),
                "last_modified_at": date(
                    *[int(n) for n in zrec["modified"][:10].split("-")]
                ),
                "resource_url": zrec["doi_url"],
                "path": f"_resources/{to_slug(metadata['title'])}.md",
                "nav_order": 1,
            }

            # Migrate custom keys from the original record
            for key, val in rec.items():
                if key not in row:
                    row[key] = val
            if not row.get("access_url"):
                row["access_url"] = row["resource_url"]

            with open(upd_path / path_.name, "w", encoding="utf-8") as f:
                yaml.safe_dump(row, f)
            print(f" Updated {path_.name}")

        else:
            # Copy non-Zenodo records as they are
            shutil.copy2(path_, upd_path)
            print(f" Copied {path_.name}")

    # Get tags from happy hours
    tagged = []
    with open(BASEPATH / "_data" / "pdwg-happy-hours.yml", encoding="utf-8") as f:
        for event in yaml.safe_load(f):
            event["url"] = f"/community/pdwg-happy-hours#{event['date']}"
            event["kind"] = "PDWG happy hour"
            event["tags"] = event.get(key, [])
            tagged.append(
                {
                    k: v
                    for k, v in event.items()
                    if k in {"title", "kind", "url", "tags"}
                }
            )

    # Construct the navigation and build a tag index using file front matter. This
    # section should generally not be modified.

    print("Reading front matter")
    fms = read_fms(BASEPATH)

    print("Determining URLs")
    compute_urls(fms)

    print("Indexing tags")
    index_tags(fms, "topics", tagged=tagged)

    print("Building navigation")
    build_nav(fms, include_main=["topics.md"], exclude_sidebar=["topics.md"])

    print("Adding glossary tooltips")
    add_tooltips(BASEPATH)
