# Contributing

Contributions are welcome. Pull requests are welcome. Forks are welcome.

## Rules for this project

**The page must stay in one file.** Do not add external JavaScript files.
Do not add external CSS files. Do not add a build step for the browser.
A user must be able to open `index.html` directly.

**Do not add external network calls.** Google Fonts is the only external
resource that the page may load. Do not add a CDN script. Do not add an
external image. Do not add an analytics script.

**Verify a formula against the server source before you add it.** Do not
guess a formula. Find the formula in the Crossfire server source code
first.

* Use `server/spell_util.cpp` for the mana cost formula and the grace
  cost formula. The function names are `SP_level_spellpoint_cost`,
  `caster_level`, and `min_casting_level`.
* Use `server/spell_attack.cpp` and `server/spell_effect.cpp` for the
  effect formulas. Search for calls to `SP_level_dam_adjust`. Each call
  shows which stat field a spell type adjusts.
* Use `server/spell_effect.cpp` for the healing formula. The function
  name is `cast_heal`. Note that a healing spell does not scale with
  caster level in the current server code. Only the grace cost scales.

**Mark uncertain data as uncertain.** Some spells trigger a second
archetype through the `other_arch` field. The rune spells are one
example. The Grimoire does not follow this chain today. Do not invent an
effect number for a spell like this. Classify the spell as `utility`
instead. A dash then shows in the effect column.

**Test the page in a browser before you open a pull request.**

1. Open the page in light mode.
2. Open the page in dark mode.
3. Type a name in the search box. Check that the table updates.
4. Select a school filter. Check that the table updates.
5. Select a path in the attunement panel. Check that the cost numbers
   and the effect numbers change for spells on that path only.
6. Scroll the table left and right. Check that the spell name column
   stays in place.

## How to rebuild the spell data

The `tools/` directory has three scripts. Run the scripts in this order.

1. Clone the [crossfire-arch](https://sourceforge.net/p/crossfire/crossfire-arch/)
   repository. This step needs the `spell/` directory from that
   repository.
2. Run `extract_spells.py`. This script reads the archetype files and
   writes `spells.json`.

   ```sh
   tools/extract_spells.py --arch-dir /path/to/crossfire-arch/spell --out spells.json
   ```
3. Run `classify.py`. This script reads `spells.json` and writes
   `spells_classified.json`. This step picks one effect type for each
   spell.

   ```sh
   tools/classify.py --in spells.json --out spells_classified.json
   ```
4. Copy the new `spells_classified.json` file into `tools/`. This file
   replaces the checked-in copy.
5. Run `build.py`. This script embeds the data into `template.html` and
   writes `index.html`.

   ```sh
   tools/build.py
   ```

## Questions

Contact Rick Tanner on the [tannerrj GitHub profile](https://github.com/tannerrj).
