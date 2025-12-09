# Chibi Fantasy 2 Inspired Character Maker

A lightweight Python CLI that recreates a nostalgic character creation flow from the classic online game **Chibi Fantasy 2**.

## Features
- Build a character by selecting species, job, hometown, fighting style, and element.
- Apply layered stat modifiers to mimic the game's early-level feel.
- Generate flavorful random characters with `--random`.
- Browse all available options with `--list`.

## Requirements
- Python 3.9+

## Usage
List all choices:
```bash
python character_creator.py --list
```

Create a specific character:
```bash
python character_creator.py \
  --name リリィ \
  --species Fairy \
  --job Mage \
  --hometown "Sky Harbor" \
  --style Mystic \
  --element Water
```

Create a character using random defaults for any missing fields:
```bash
python character_creator.py --species Human --job Warrior --random
```
