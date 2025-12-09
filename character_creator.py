"""
Character creation system inspired by the nostalgic online game "Chibi Fantasy 2".

The script supports two main flows:
- Generate a character directly via command-line flags.
- Explore the available options (races, jobs, hometowns, fighting styles) via --list.

Example:
    python character_creator.py --name リリィ --species Fairy --job Mage \
        --hometown "Sky Harbor" --style Mystic --element Water

Use --random to fill in any missing choices with flavorful defaults that match the world.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field
from typing import Dict, List

STATS = ["HP", "MP", "STR", "INT", "AGI", "VIT", "MND", "LUK"]

SPECIES: Dict[str, Dict[str, object]] = {
    "Human": {
        "description": "Balanced adventurers adaptable to any role.",
        "base": {"HP": 22, "MP": 12, "STR": 10, "INT": 10, "AGI": 10, "VIT": 10, "MND": 10, "LUK": 11},
    },
    "Elf": {
        "description": "Graceful spellcasters with sharp senses.",
        "base": {"HP": 18, "MP": 18, "STR": 8, "INT": 13, "AGI": 12, "VIT": 9, "MND": 12, "LUK": 12},
    },
    "Dwarf": {
        "description": "Stout guardians who trust in armor and hammers.",
        "base": {"HP": 26, "MP": 8, "STR": 13, "INT": 8, "AGI": 8, "VIT": 13, "MND": 9, "LUK": 9},
    },
    "Fairy": {
        "description": "Tiny allies with quick wings and endless curiosity.",
        "base": {"HP": 16, "MP": 20, "STR": 6, "INT": 14, "AGI": 14, "VIT": 8, "MND": 12, "LUK": 14},
    },
    "Dragonkin": {
        "description": "Ancient blood grants fiery might and resilience.",
        "base": {"HP": 28, "MP": 12, "STR": 14, "INT": 10, "AGI": 9, "VIT": 14, "MND": 10, "LUK": 8},
    },
}

JOBS: Dict[str, Dict[str, object]] = {
    "Warrior": {
        "description": "Front-line fighter who values strength and armor.",
        "mods": {"HP": +4, "STR": +4, "VIT": +3, "AGI": -1, "MP": -2},
    },
    "Mage": {
        "description": "Arcane scholar wielding elemental spirits.",
        "mods": {"MP": +6, "INT": +4, "MND": +3, "HP": -2, "STR": -2},
    },
    "Thief": {
        "description": "Agile scout who excels at critical strikes.",
        "mods": {"AGI": +5, "LUK": +3, "STR": +1, "HP": -1, "MP": -1},
    },
    "Priest": {
        "description": "Guardian of light who protects and heals allies.",
        "mods": {"MP": +3, "MND": +5, "HP": +1, "STR": -1, "AGI": -1},
    },
    "Ranger": {
        "description": "Hunter who dances between bowshots and traps.",
        "mods": {"AGI": +3, "STR": +2, "LUK": +2, "INT": +1, "HP": +1},
    },
    "Ronin": {
        "description": "Wandering blade that balances offense and focus.",
        "mods": {"STR": +3, "AGI": +2, "MND": +1, "HP": +2, "MP": -1},
    },
}

HOMETOWNS: Dict[str, Dict[str, object]] = {
    "Sunrise Village": {
        "flavor": "A calm farming town; residents learn patience and grit.",
        "mods": {"HP": +1, "VIT": +1, "LUK": +1},
    },
    "Lunaris Academy": {
        "flavor": "A floating academy that trains elemental adepts.",
        "mods": {"MP": +2, "INT": +2},
    },
    "Ironforge Depot": {
        "flavor": "Railway stop built inside an old mine.",
        "mods": {"STR": +1, "VIT": +2},
    },
    "Sky Harbor": {
        "flavor": "Port in the clouds where skyfishers trade rarities.",
        "mods": {"AGI": +2, "LUK": +1},
    },
    "Verdant Shrine": {
        "flavor": "Sacred grove rumored to shelter a tiny dragon deity.",
        "mods": {"MND": +2, "MP": +1},
    },
}

STYLES: Dict[str, Dict[str, object]] = {
    "Balanced": {
        "tagline": "Safe choice for new players; keeps stats steady.",
        "mods": {"HP": +1, "MP": +1, "STR": +1, "INT": +1, "AGI": +1, "VIT": +1, "MND": +1, "LUK": +1},
    },
    "Aggressive": {
        "tagline": "Pours everything into offense; fragile but explosive.",
        "mods": {"STR": +3, "AGI": +2, "HP": -1, "VIT": -1, "MND": -1},
    },
    "Mystic": {
        "tagline": "Favors magic and technique over raw might.",
        "mods": {"INT": +3, "MP": +3, "MND": +2, "STR": -2},
    },
    "Defender": {
        "tagline": "Shields allies, soaking up every attack.",
        "mods": {"HP": +3, "VIT": +3, "STR": +1, "AGI": -2},
    },
    "Trickster": {
        "tagline": "Lives for critical hits and rare drops.",
        "mods": {"LUK": +4, "AGI": +1, "INT": +1, "HP": -1},
    },
}

ELEMENTS = ["Fire", "Water", "Wind", "Earth", "Light", "Dark"]


@dataclass
class Character:
    name: str
    species: str
    job: str
    hometown: str
    style: str
    element: str
    stats: Dict[str, int] = field(default_factory=dict)

    def describe(self) -> str:
        """Return a multi-line description of the character."""
        lines: List[str] = [
            f"Name      : {self.name}",
            f"Species   : {self.species} — {SPECIES[self.species]['description']}",
            f"Job       : {self.job} — {JOBS[self.job]['description']}",
            f"Hometown  : {self.hometown} — {HOMETOWNS[self.hometown]['flavor']}",
            f"Style     : {self.style} — {STYLES[self.style]['tagline']}",
            f"Element   : {self.element}",
            "Stats:",
        ]
        widest = max(len(stat) for stat in STATS)
        for stat in STATS:
            lines.append(f"  {stat.ljust(widest)} : {self.stats.get(stat, 0)}")
        return "\n".join(lines)


def apply_mods(base: Dict[str, int], *mods: Dict[str, int]) -> Dict[str, int]:
    """Return a new stats dict with sequential modifiers applied."""
    result = dict(base)
    for mod in mods:
        for key, value in mod.items():
            result[key] = result.get(key, 0) + value
    # Keep stats sensible for a low-level character
    for key in STATS:
        result[key] = max(1, result[key])
    return result


def generate_character(
    *,
    name: str,
    species: str,
    job: str,
    hometown: str,
    style: str,
    element: str,
) -> Character:
    stats = apply_mods(
        SPECIES[species]["base"],
        JOBS[job]["mods"],
        HOMETOWNS[hometown]["mods"],
        STYLES[style]["mods"],
    )
    return Character(
        name=name,
        species=species,
        job=job,
        hometown=hometown,
        style=style,
        element=element,
        stats=stats,
    )


def pick_random_choice(mapping: Dict[str, Dict[str, object]]) -> str:
    return random.choice(list(mapping.keys()))


def random_name() -> str:
    syllables = ["ri", "na", "to", "mi", "ka", "yu", "se", "ra", "lo", "fi", "ta", "ko", "e", "an", "lu"]
    return "".join(random.choice(syllables).capitalize() for _ in range(2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chibi Fantasy 2 style character maker")
    parser.add_argument("--name", help="Character name (defaults to generated)")
    parser.add_argument("--species", choices=SPECIES.keys(), help="Select a species")
    parser.add_argument("--job", choices=JOBS.keys(), help="Choose a job")
    parser.add_argument("--hometown", choices=HOMETOWNS.keys(), help="Origin town")
    parser.add_argument("--style", choices=STYLES.keys(), help="Combat style")
    parser.add_argument("--element", choices=ELEMENTS, help="Elemental affinity")
    parser.add_argument("--list", action="store_true", help="List all available options")
    parser.add_argument(
        "--random",
        action="store_true",
        help="Fill any missing fields with flavorful random values",
    )
    return parser.parse_args()


def list_options() -> str:
    lines: List[str] = []
    lines.append("Species:")
    for name, info in SPECIES.items():
        lines.append(f"- {name}: {info['description']}")
    lines.append("\nJobs:")
    for name, info in JOBS.items():
        lines.append(f"- {name}: {info['description']}")
    lines.append("\nHometowns:")
    for name, info in HOMETOWNS.items():
        lines.append(f"- {name}: {info['flavor']}")
    lines.append("\nStyles:")
    for name, info in STYLES.items():
        lines.append(f"- {name}: {info['tagline']}")
    lines.append("\nElements:")
    lines.extend(f"- {element}" for element in ELEMENTS)
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    if args.list:
        print(list_options())
        return

    name = args.name or random_name()
    species = args.species
    job = args.job
    hometown = args.hometown
    style = args.style
    element = args.element

    if args.random:
        species = species or pick_random_choice(SPECIES)
        job = job or pick_random_choice(JOBS)
        hometown = hometown or pick_random_choice(HOMETOWNS)
        style = style or pick_random_choice(STYLES)
        element = element or random.choice(ELEMENTS)

    missing_fields = [
        field_name
        for field_name, value in [
            ("species", species),
            ("job", job),
            ("hometown", hometown),
            ("style", style),
            ("element", element),
        ]
        if value is None
    ]
    if missing_fields:
        raise SystemExit(
            "Missing required fields: "
            + ", ".join(missing_fields)
            + ". Provide them directly or use --random to fill in the rest."
        )

    character = generate_character(
        name=name,
        species=species,
        job=job,
        hometown=hometown,
        style=style,
        element=element,
    )
    print(character.describe())


if __name__ == "__main__":
    main()
