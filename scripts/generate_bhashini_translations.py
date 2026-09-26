#!/usr/bin/env python3
"""
Generate Bhashini-powered Flutter locale files from en.json.

Reads:
    frontend/assets/translations/en.json

Writes:
    frontend/assets/translations/<locale>.json

Usage:
    python scripts/generate_bhashini_translations.py \
        --backend-url http://localhost:8000 \
        --source frontend/assets/translations/en.json \
        --target-dir frontend/assets/translations \
        --locales hi bn ta

Environment:
    BHASHINI_API_URL  optional override for backend URL
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_BACKEND_URL = os.getenv("BHASHINI_API_URL", "http://localhost:8000")
TRANSLATE_ENDPOINT = "/api/v1/bhashini/translate"
CONCURRENCY = 5
TIMEOUT = 60.0
MAX_RETRIES = 3

# Keys that must not be translated
SKIP_KEYS = {
    "app_name",
    "tagline",
    "app_tagline_full",
}

# Placeholder pattern
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
# Token format used inside protected strings
PLACEHOLDER_TOKEN_RE = re.compile(r"<ph(\d+)>")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json_atomic(path: Path, data: Dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp.json")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)


def extract_translatable(
    source: Dict[str, Any],
) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for key, value in source.items():
        if not isinstance(value, str):
            continue
        if key in SKIP_KEYS:
            continue
        items.append((key, value))
    return items


def validate_placeholders(original: str, translated: str) -> bool:
    orig_set = set(PLACEHOLDER_RE.findall(original))
    trans_set = set(PLACEHOLDER_RE.findall(translated))
    return orig_set == trans_set


# ---------------------------------------------------------------------------
# Translation with placeholder protection
# ---------------------------------------------------------------------------


def protect_placeholders(text: str) -> Tuple[str, Dict[str, str]]:
    """Replace placeholders with short numeric tokens unlikely to be altered."""
    mapping: Dict[str, str] = {}
    tokens = PLACEHOLDER_RE.findall(text)
    for i, token in enumerate(tokens):
        key = f"§{i}§"
        mapping[key] = token
        text = text.replace(token, key, 1)
    return text, mapping


def restore_placeholders(text: str, mapping: Dict[str, str]) -> str:
    """Restore placeholders after translation.

    Bhashini may insert spaces around or reorder the token, so we
    match multiple variants: §0§, § 0 §, §0 §, 0 §, ₹0 §, etc.
    """
    for key, token in mapping.items():
        if key in text:
            text = text.replace(key, token)
            continue
        idx = key.strip("§")
        # Match various spaced/reordered variants Bhashini may produce
        for pattern in [
            f"§ {idx} §",   # § 0 §
            f"§{idx} §",    # §0 §
            f"§ {idx}§",    # § 0§
            rf"[₹$€£]?\s*{idx}\s*§",  # ₹0 § or 0 §
            rf"§\s*{idx}",  # §0
        ]:
            text = re.sub(pattern, token, text)
    return text


async def translate_text(
    client: httpx.AsyncClient,
    backend_url: str,
    text: str,
    source_language: str,
    target_language: str,
) -> str:
    """Translate a single string, preserving placeholders."""
    if not text.strip():
        return text

    protected_text, placeholder_map = protect_placeholders(text)

    for attempt in range(MAX_RETRIES):
        try:
            resp = await client.post(
                f"{backend_url}{TRANSLATE_ENDPOINT}",
                params={
                    "text": protected_text,
                    "source_language": source_language,
                    "target_language": target_language,
                },
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            translated = data.get("translated_text", "")
            if not translated:
                raise ValueError("Empty translation")
            return restore_placeholders(translated, placeholder_map)
        except (httpx.HTTPError, ValueError) as exc:
            if attempt == MAX_RETRIES - 1:
                print(
                    f"  ERROR translating '{text[:40]}...': {exc}",
                    file=sys.stderr,
                )
                raise
            await asyncio.sleep(2 ** attempt)
    return text  # fallback


async def translate_locale(
    client: httpx.AsyncClient,
    backend_url: str,
    source_map: Dict[str, str],
    source_language: str,
    target_language: str,
) -> Dict[str, str]:
    """Translate all strings for one target locale with concurrency limit."""
    items = extract_translatable(source_map)
    semaphore = asyncio.Semaphore(CONCURRENCY)
    results: Dict[str, str] = {}

    async def _translate(key: str, value: str) -> Tuple[str, str]:
        async with semaphore:
            try:
                translated = await translate_text(
                    client, backend_url, value, source_language, target_language
                )
            except RuntimeError:
                translated = value
            return key, translated

    tasks = [_translate(key, value) for key, value in items]
    for coro in asyncio.as_completed(tasks):
        key, translated = await coro
        results[key] = translated

    return results


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def build_report(
    locale: str,
    status: str,
    keys_translated: int,
    missing_keys: int,
    placeholder_mismatches: int,
    voice_asr: bool,
    voice_tts: bool,
) -> Dict[str, Any]:
    return {
        "locale": locale,
        "status": status,
        "keys_translated": keys_translated,
        "missing_keys": missing_keys,
        "placeholder_mismatches": placeholder_mismatches,
        "voice_asr": voice_asr,
        "voice_tts": voice_tts,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Bhashini-powered Flutter locale files."
    )
    parser.add_argument(
        "--backend-url",
        default=DEFAULT_BACKEND_URL,
        help="Craftsy backend URL (default: %(default)s)",
    )
    parser.add_argument(
        "--source",
        default="frontend/assets/translations/en.json",
        help="Source English JSON file",
    )
    parser.add_argument(
        "--target-dir",
        default="frontend/assets/translations",
        help="Directory for generated locale files",
    )
    parser.add_argument(
        "--locales",
        nargs="+",
        required=True,
        help="Target locale codes, e.g. hi bn ta",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan without writing files",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    target_dir = Path(args.target_dir)
    backend_url = args.backend_url.rstrip("/")

    if not source_path.exists():
        print(f"ERROR: source file not found: {source_path}", file=sys.stderr)
        return 1

    source_map = load_json(source_path)
    items = extract_translatable(source_map)
    total_keys = len(items)
    print(f"Source: {source_path} ({total_keys} translatable keys)")

    # Load Bhashini capabilities for voice status
    caps: Dict[str, Dict[str, Any]] = {}
    caps_path = Path("backend/routers/bhashini.py")
    if caps_path.exists():
        text = caps_path.read_text(encoding="utf-8")
        for m in re.finditer(
            r'"([a-z]{2,4})":\s*\{[^}]*?"asr":\s*(True|False)[^}]*?"tts":\s*(True|False)',
            text,
            re.DOTALL,
        ):
            code = m.group(1)
            caps[code] = {
                "asr": m.group(2) == "True",
                "tts": m.group(3) == "True",
            }

    report = []
    async with httpx.AsyncClient() as client:
        for locale in args.locales:
            print(f"\nLocale: {locale}")
            if locale == "en":
                if not args.dry_run:
                    save_json_atomic(target_dir / f"{locale}.json", source_map)
                report.append(
                    build_report(
                        locale=locale,
                        status="VERIFIED",
                        keys_translated=total_keys,
                        missing_keys=0,
                        placeholder_mismatches=0,
                        voice_asr=caps.get(locale, {}).get("asr", False),
                        voice_tts=caps.get(locale, {}).get("tts", False),
                    )
                )
                continue

            try:
                translations = await translate_locale(
                    client=client,
                    backend_url=backend_url,
                    source_map=source_map,
                    source_language="en",
                    target_language=locale,
                )
            except RuntimeError as exc:
                print(f"  FAILED: {exc}", file=sys.stderr)
                report.append(
                    build_report(
                        locale=locale,
                        status="UNAVAILABLE",
                        keys_translated=0,
                        missing_keys=total_keys,
                        placeholder_mismatches=0,
                        voice_asr=caps.get(locale, {}).get("asr", False),
                        voice_tts=caps.get(locale, {}).get("tts", False),
                    )
                )
                continue

            missing = total_keys - len(translations)
            mismatches = 0
            for k, v in source_map.items():
                if isinstance(v, str) and k in translations:
                    if not validate_placeholders(v, translations[k]):
                        mismatches += 1

            output = dict(source_map)
            output.update(translations)

            if not args.dry_run:
                save_json_atomic(target_dir / f"{locale}.json", output)

            status = "VERIFIED" if missing == 0 and mismatches == 0 else "PARTIAL"
            report.append(
                build_report(
                    locale=locale,
                    status=status,
                    keys_translated=len(translations),
                    missing_keys=missing,
                    placeholder_mismatches=mismatches,
                    voice_asr=caps.get(locale, {}).get("asr", False),
                    voice_tts=caps.get(locale, {}).get("tts", False),
                )
            )
            print(
                f"  status={status} translated={len(translations)} "
                f"missing={missing} mismatches={mismatches}"
            )

    print("\n=== Translation Report ===")
    for r in report:
        print(
            f"{r['locale']:6s} | {r['status']:10s} | "
            f"keys={r['keys_translated']} missing={r['missing_keys']} "
            f"mismatches={r['placeholder_mismatches']} | "
            f"ASR={r['voice_asr']} TTS={r['voice_tts']}"
        )

    report_path = target_dir / "translation_report.json"
    if not args.dry_run:
        save_json_atomic(report_path, {"locales": report})
    print(f"\nReport written to {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
