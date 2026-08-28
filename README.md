# Crossfire Grimoire

The Crossfire Grimoire is a web page. The page shows data for all spells
and prayers in the [Crossfire](https://crossfire.real-time.com/) game. The
page shows the mana cost, the grace cost, and the effect value for each
spell. The page shows this data for character levels 1 to 115.

## Purpose

A player must know the cost and the effect of a spell before the player
learns it. The Crossfire server calculates this data at run time. The
server does not show a table of this data to the player.

The Grimoire calculates the same data ahead of time. The Grimoire shows
the data in one table. A player can compare spells before the player
spends experience points on them.

## Data source

The Grimoire does not guess spell data. The Grimoire reads the archetype
files from the [crossfire-arch](https://sourceforge.net/p/crossfire/crossfire-arch/)
repository. The Grimoire applies the same formulas as the Crossfire
server. The formulas come from these files in the
[crossfire-server](https://sourceforge.net/p/crossfire/crossfire-server/)
repository:

* `server/spell_util.cpp`
* `server/spell_attack.cpp`
* `server/spell_effect.cpp`

See CONTRIBUTING.md for the exact function names and the rules for each
spell type.

## Features

* **Search.** Type a name in the search box. The table shows only the
  spells that match the name.
* **School filters.** Select a school button. The table shows only the
  spells from that school. A player can select more than one school.
* **Effect filters.** Select an effect button. The table shows only the
  spells with that effect type. Damage, healing, and resistance are
  examples of an effect type.
* **Level jump.** Type a level number in the box. Select the Go button.
  The table scrolls to that level column.
* **Path attunement panel.** Select a path name in the panel. The path
  name changes state: neutral, attuned, or repelled. The table updates
  the cost and the effect for every spell on that path. A character's
  god or relic grants this kind of attunement in the game.

## Requirements

A web browser with JavaScript enabled. The Grimoire needs no other
software.

## Usage

Open `index.html` in a web browser. The page is self-contained. The page
needs no server and no internet connection, except for two font files
from Google Fonts.

## Live web page

* [The Grimoire (Claude Artifact)](https://claude.ai/code/artifact/44eccf67-65a8-452d-902e-6f4af46d2510)

## Rebuilding the data

The `tools/` directory has the scripts that build `index.html`. See
CONTRIBUTING.md for the steps.

## Contributing

See CONTRIBUTING.md for the rules for this project.

## Questions

Contact Rick Tanner on the [tannerrj GitHub profile](https://github.com/tannerrj).

## License

MIT License. See the LICENSE file.

## Crossfire social media links

* [BlueSky](https://bsky.app/profile/crossfireproject.bsky.social)
* [Facebook](https://www.facebook.com/crossfireproject/)
* [Mastodon](https://mastodon.social/@crossfiremrpg)
* [X (Formerly Twitter)](https://twitter.com/crossfiremrpg/)
