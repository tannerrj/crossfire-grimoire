#!/usr/bin/env python3
"""Turn raw spell data into display data for the Grimoire page.

Usage:
    tools/classify.py --in spells.json --out spells_classified.json

The script reads the output of extract_spells.py. For each spell, the
script picks one effect type: damage, heal, resist, stat, and so on.
The script also picks one number as the effect base value.

The rules in this script come from the Crossfire server source. See
CONTRIBUTING.md for the file names and the function names to check.
"""
import argparse
import json
from collections import Counter

DAMAGE_FOLDERS = {
    "Bolt", "Bullet", "Cone", "MovingBall", "Swarm", "Bomb",
    "Smite", "MagicWall", "Rune", "Aura", "MagicMissile",
}
SUMMON_FOLDERS = {"Golem", "SummonMonster", "AnimateWeapon"}

SCHOOL_NAMES = {
    "sorcery": "Sorcery",
    "pyromancy": "Pyromancy",
    "evocation": "Evocation",
    "summoning": "Summoning",
    "praying": "Praying",
}

# A few Misc-folder spells move mana or grace directly, or count items,
# instead of doing damage. The server code confirms each one by name:
# cast_transfer(), cast_identify(), cast_create_missile() in
# server/spell_effect.cpp.
MISC_SPECIAL = {
    "transference": ("transfer", "SP drained from target (to self)"),
    "magic drain": ("transfer", "SP drained from caster's mana pool"),
    "identify": ("count", "Items identified"),
    "create missile": ("enchant", "Bonus enchantment on created ammo"),
}


def classify(spell):
    """Pick one effect type and one base value for a spell."""
    folder = spell["folder"]
    dam = spell["dam"]
    hp = spell["hp"]
    resists = spell["resists"]
    stats = spell["stats"]

    multi = sum([bool(resists), bool(stats), bool(hp)]) > 1

    if spell["name"] in MISC_SPECIAL and folder == "Misc":
        effect_type, label = MISC_SPECIAL[spell["name"]]
        return {"type": effect_type, "label": label, "base": abs(dam), "multi": False}

    if folder == "Healing":
        if dam >= 9999:
            return {"type": "fullheal", "label": "Full heal", "multi": False}
        if not dam and not hp:
            return {
                "type": "utility",
                "label": "Cures a status effect (no HP restored)",
                "multi": False,
            }
        average = dam + (hp * 3.5 + hp if hp else 0)
        return {"type": "heal", "label": "Healing (avg HP)", "value": round(average, 1), "multi": False}

    if resists:
        key = max(resists, key=lambda name: resists[name])
        label = f"{key.replace('_', ' ').title()} resistance"
        return {"type": "resist", "label": label, "base": resists[key], "multi": multi}

    if stats and folder == "Change_Ability":
        key = max(stats, key=lambda name: stats[name])
        return {"type": "stat", "label": f"{key} bonus (flat, random)", "base": stats[key], "multi": multi}

    if hp and folder == "Change_Ability":
        return {"type": "hpbonus", "label": "Max HP bonus", "base": hp, "multi": multi}

    if dam and folder in DAMAGE_FOLDERS:
        return {"type": "damage", "label": "Damage", "base": dam, "multi": multi}

    if dam and folder in SUMMON_FOLDERS:
        return {"type": "summon", "label": "Summon power", "base": dam, "multi": multi}

    return {"type": "utility", "label": "Utility (no scaled magnitude)", "multi": multi}


def path_value(raw):
    text = str(raw).strip().lstrip("-")
    return int(raw) if text.isdigit() else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="in_path", default="spells.json")
    parser.add_argument("--out", dest="out_path", default="spells_classified.json")
    args = parser.parse_args()

    data = json.load(open(args.in_path, encoding="utf-8"))
    out = []
    for spell in data:
        effect = classify(spell)
        out.append({
            "name": spell["name"],
            "category": "Prayer" if spell["skill"] == "praying" else "Spell",
            "school": SCHOOL_NAMES[spell["skill"]],
            "level": spell["level"],
            "sp": spell["sp"],
            "maxsp": spell["maxsp"],
            "grace": spell["grace"],
            "maxgrace": spell["maxgrace"],
            "dam_modifier": spell["dam_modifier"],
            "path": path_value(spell["path_attuned"]),
            "effect": effect,
        })

    out.sort(key=lambda entry: (entry["category"], entry["school"], entry["level"], entry["name"]))
    with open(args.out_path, "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=1)

    print(f"Wrote {args.out_path} ({len(out)} spells and prayers)")
    print(Counter(entry["effect"]["type"] for entry in out))


if __name__ == "__main__":
    main()
