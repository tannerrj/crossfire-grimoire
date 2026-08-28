#!/usr/bin/env python3
"""Extract raw spell and prayer data from Crossfire archetype files.

Usage:
    tools/extract_spells.py --arch-dir /path/to/crossfire-arch/spell --out spells.json

The script needs a checkout of the crossfire-arch repository. Get it here:
    https://sourceforge.net/p/crossfire/crossfire-arch/

The script reads every .arc file under the spell directory. The script
keeps an object only if the object has a "skill" field with a value of
sorcery, pyromancy, evocation, summoning, or praying. The script drops
monster-only objects and the Ability/ folder, because players cannot
learn spells from these.

The output is a JSON file. Each entry has the raw fields for one spell
or prayer. Run classify.py next to turn this into display data.
"""
import argparse
import glob
import json
import os
import re

VALID_SKILLS = {"evocation", "pyromancy", "sorcery", "summoning", "praying"}
STAT_FIELDS = ("Str", "Dex", "Con", "Wis", "Pow", "Cha", "Int")


def parse_arc(path):
    """Parse one .arc file. Return a list of top-level Object blocks.

    The parser skips the text inside msg/endmsg blocks.
    """
    objects = []
    current = None
    in_msg = False
    with open(path, "r", errors="replace") as handle:
        for line in handle:
            stripped = line.strip()
            if in_msg:
                if stripped == "endmsg":
                    in_msg = False
                continue
            if stripped.startswith("Object "):
                current = {"_name": stripped.split(None, 1)[1], "_file": path}
                continue
            if stripped == "end":
                if current is not None:
                    objects.append(current)
                current = None
                continue
            if stripped == "msg":
                in_msg = True
                continue
            if current is None:
                continue
            match = re.match(r"^(\S+)\s*(.*)$", stripped)
            if not match:
                continue
            key, value = match.group(1), match.group(2)
            current[key] = value
    return objects


def to_int(value, default=0):
    """Convert a string field to an int. Return the default on failure."""
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default


def is_castable_spell(obj):
    """Return True if a player can learn and cast this object as a spell."""
    skill = obj.get("skill", "").strip()
    if skill not in VALID_SKILLS:
        return False
    if "level" not in obj:
        return False
    if to_int(obj.get("monster", "0")):
        return False
    return True


def build_entry(obj, arch_dir):
    rel_path = os.path.relpath(obj["_file"], arch_dir)
    resists = {
        key[len("resist_"):]: to_int(value)
        for key, value in obj.items()
        if key.startswith("resist_") and to_int(value)
    }
    stats = {
        field: to_int(obj.get(field))
        for field in STAT_FIELDS
        if to_int(obj.get(field))
    }
    return {
        "arch": obj["_name"],
        "name": obj.get("name", obj["_name"]).strip(),
        "folder": rel_path.split(os.sep)[0],
        "file": rel_path,
        "skill": obj.get("skill", "").strip(),
        "level": to_int(obj.get("level")),
        "sp": to_int(obj.get("sp")),
        "maxsp": to_int(obj.get("maxsp")),
        "grace": to_int(obj.get("grace")),
        "maxgrace": to_int(obj.get("maxgrace")),
        "dam": to_int(obj.get("dam")),
        "dam_modifier": to_int(obj.get("dam_modifier")),
        "hp": to_int(obj.get("hp")),
        "ac": to_int(obj.get("ac")),
        "resists": resists,
        "stats": stats,
        "duration": to_int(obj.get("duration")),
        "duration_modifier": to_int(obj.get("duration_modifier")),
        "range": to_int(obj.get("range")),
        "range_modifier": to_int(obj.get("range_modifier")),
        "other_arch": obj.get("other_arch", ""),
        "path_attuned": obj.get("path_attuned", ""),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--arch-dir",
        required=True,
        help="Path to the spell/ directory inside a crossfire-arch checkout",
    )
    parser.add_argument(
        "--out",
        default="spells.json",
        help="Output file path (default: spells.json)",
    )
    args = parser.parse_args()

    pattern = os.path.join(args.arch_dir, "**", "*.arc")
    spells = []
    for path in glob.glob(pattern, recursive=True):
        for obj in parse_arc(path):
            if not is_castable_spell(obj):
                continue
            rel = os.path.relpath(path, args.arch_dir)
            if rel.startswith("Ability" + os.sep):
                continue
            spells.append(build_entry(obj, args.arch_dir))

    spells.sort(key=lambda entry: (entry["skill"], entry["level"], entry["name"]))
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(spells, handle, indent=1)
    print(f"Wrote {args.out} ({len(spells)} spells and prayers)")


if __name__ == "__main__":
    main()
