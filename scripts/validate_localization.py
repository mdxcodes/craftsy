#!/usr/bin/env python3
"""
Localization validation script for Craftsy.

Checks:
- All locale files have the same key set
- No missing keys
- No extra keys
- No empty values
- Valid JSON syntax

Usage:
    python scripts/validate_localization.py
    python scripts/validate_localization.py --path frontend/assets/translations
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_translations(path: Path) -> dict[str, dict[str, str]]:
    """Load all JSON translation files from directory."""
    translations = {}
    for file in path.glob("*.json"):
        locale = file.stem
        try:
            with open(file, encoding="utf-8") as f:
                translations[locale] = json.load(f)
        except json.JSONDecodeError as exc:
            print(f"ERROR: {file}: Invalid JSON: {exc}")
            sys.exit(1)
    return translations


def validate(translations: dict[str, dict[str, str]]) -> bool:
    """Validate all translation files."""
    locales = sorted(translations.keys())
    if not locales:
        print("ERROR: No translation files found.")
        return False

    reference = locales[0]
    reference_keys = set(translations[reference].keys())
    all_ok = True

    print(f"Locales: {locales}")
    print(f"Reference: {reference} ({len(reference_keys)} keys)")
    print()

    for locale in locales[1:]:
        keys = set(translations[locale].keys())
        missing = reference_keys - keys
        extra = keys - reference_keys
        empty = [k for k in keys if not translations[locale][k].strip()]

        if missing or extra or empty:
            all_ok = False

        if missing:
            print(f"FAIL [{locale}]: Missing {len(missing)} keys:")
            for k in sorted(missing)[:20]:
                print(f"  - {k}")
            if len(missing) > 20:
                print(f"  ... and {len(missing) - 20} more")

        if extra:
            print(f"FAIL [{locale}]: Extra {len(extra)} keys:")
            for k in sorted(extra)[:20]:
                print(f"  + {k}")
            if len(extra) > 20:
                print(f"  ... and {len(extra) - 20} more")

        if empty:
            print(f"WARN [{locale}]: {len(empty)} empty values:")
            for k in sorted(empty)[:10]:
                print(f"  ! {k}")
            if len(empty) > 10:
                print(f"  ... and {len(empty) - 10} more")

        if not missing and not extra and not empty:
            print(f"PASS [{locale}]: All {len(keys)} keys match reference.")

    print()
    for locale in locales:
        total = len(translations[locale])
        empty = sum(1 for v in translations[locale].values() if not v.strip())
        print(f"  {locale}: {total} keys, {empty} empty values")

    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Craftsy localization files.")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("frontend/assets/translations"),
        help="Path to translation files directory",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: Path not found: {args.path}")
        sys.exit(1)

    translations = load_translations(args.path)
    ok = validate(translations)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
