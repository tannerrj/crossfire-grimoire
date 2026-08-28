#!/usr/bin/env python3
"""Build index.html from template.html and spells_classified.json.

Usage:
    tools/build.py

The script does two things:
1. It embeds the spell data as JSON into the template.
2. It wraps the result in a full HTML document.

The output file is index.html, in the project root.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TEMPLATE_PATH = os.path.join(HERE, "template.html")
DATA_PATH = os.path.join(HERE, "spells_classified.json")
OUTPUT_PATH = os.path.join(ROOT, "index.html")


def build():
    template = open(TEMPLATE_PATH, "r", encoding="utf-8").read()
    data = json.load(open(DATA_PATH, "r", encoding="utf-8"))
    data_json = json.dumps(data, separators=(",", ":"))

    if "__SPELLS_JSON__" not in template:
        raise SystemExit("template.html has no __SPELLS_JSON__ placeholder")
    page = template.replace("__SPELLS_JSON__", data_json)

    style_close = "</style>"
    idx = page.index(style_close) + len(style_close)
    head = page[:idx]
    body = page[idx:]

    doc = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"{head}\n"
        "</head>\n"
        "<body>\n"
        f"{body}\n"
        "</body>\n"
        "</html>\n"
    )

    open(OUTPUT_PATH, "w", encoding="utf-8").write(doc)
    print(f"Wrote {OUTPUT_PATH} ({len(doc)} bytes, {len(data)} spells)")


if __name__ == "__main__":
    build()
