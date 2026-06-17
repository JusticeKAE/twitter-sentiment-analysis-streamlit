#!/usr/bin/env python3
"""Convert TweetClaw exports to the app's upload CSV format."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

TEXT_KEYS = ("tweet", "text", "full_text", "tweet_text", "content", "body")
LIST_KEYS = ("tweets", "items", "data", "results")
NESTED_KEYS = ("tweet", "tweet_data", "raw", "node")


def normalize_records(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in LIST_KEYS:
            nested = value.get(key)
            if isinstance(nested, list):
                return nested
        return [value]
    return [value]


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_jsonl(raw_text: str) -> List[Any]:
    rows = []
    for line_number, line in enumerate(raw_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            rows.append(json.loads(stripped))
        except json.JSONDecodeError as error:
            raise ValueError(f"Line {line_number} is not valid JSON") from error
    return rows


def load_records(path: Path) -> List[Any]:
    if path.suffix.lower() == ".csv":
        return load_csv(path)

    raw_text = path.read_text(encoding="utf-8")
    try:
        return normalize_records(json.loads(raw_text))
    except json.JSONDecodeError:
        return load_jsonl(raw_text)


def extract_text(record: Any) -> Optional[str]:
    if isinstance(record, str):
        return record.strip() or None

    if not isinstance(record, dict):
        return None

    for key in TEXT_KEYS:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    for key in NESTED_KEYS:
        value = record.get(key)
        if isinstance(value, dict):
            nested_text = extract_text(value)
            if nested_text:
                return nested_text

    return None


def write_tweets(path: Path, tweets: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["tweet"])
        writer.writeheader()
        for tweet in tweets:
            writer.writerow({"tweet": tweet})


def convert(source: Path, destination: Path) -> int:
    records = load_records(source)
    tweets = []
    for record in records:
        tweet = extract_text(record)
        if tweet:
            tweets.append(tweet)

    if not tweets:
        raise ValueError("No tweet text found. Expected a tweet, text, or full_text field.")

    write_tweets(destination, tweets)
    return len(tweets)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Convert TweetClaw JSON, JSONL, or CSV exports to a CSV with a tweet column."
    )
    parser.add_argument("source", help="TweetClaw export path")
    parser.add_argument("destination", help="Output CSV path for the Streamlit uploader")
    args = parser.parse_args(argv)

    try:
        count = convert(Path(args.source), Path(args.destination))
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Wrote {count} tweets to {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
